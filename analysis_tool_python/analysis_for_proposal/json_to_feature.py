import json
import hashlib
from os import path as os_path
from collections import OrderedDict
from analysis_tool_python.util import load_file, cfg

FEATURE_PATH = "./feature_json/"


class FeatureJsonConverter:
    def __init__(self, feature_path=FEATURE_PATH):
        # paths[0=canonical, 1=bc, 2=uncle, 3=forked][0=raw_path, 1=json_path]
        self.paths = cfg.load_cfg()
        # files_md5[file_type][filename] = md5
        self.files_md5 = dict()
        self.feature_path = feature_path
        self.file_types = {0: "canonical", 1: "broadcast", 2: "uncle", 3: "forked"}
        self.done_count = 0

    def run(self):
        self.load_md5(self.feature_path)
        filename_updated = dict()
        total_count = 0
        for idx_type in range(len(self.paths)):
            path = self.paths[idx_type][1]
            for each in load_file.load_path(path):
                total_count += 1
        for idx_type in range(len(self.paths)):
            path = self.paths[idx_type][1]
            for filename in load_file.load_path(path):
                print(f"==== processing: finished {self.done_count / total_count * 100.0}% ====")
                if filename in filename_updated:
                    continue
                else:
                    self.check_md5(path, filename, self.file_types[idx_type])
                    filename_updated[filename] = 1
        self.dump_md5(self.feature_path)

    def load_md5(self, path):
        if os_path.exists(path + 'md5.txt'):
            with open(path + "md5.txt", 'r') as f:
                self.files_md5 = json.loads(f.read())
        else:
            self.files_md5 = {"canonical": dict(), "broadcast": dict(), "uncle": dict(), "forked": dict()}

    def dump_md5(self, path):
        with open(path + "md5.txt", 'w') as f:
            f.write(json.dumps(self.files_md5))

    def check_md5(self, path, filename, file_type):
        feature_md5 = self.cal_md5(path + filename)
        if filename in self.files_md5[file_type] \
                and self.files_md5[file_type][filename] == feature_md5:
            print(f"{filename}: md5 check succeeds")
            self.done_count += 1
            return
        else:
            self.convert_raw_to_feature(filename)

    @staticmethod
    def cal_md5(path):
        md5_hash = hashlib.md5()
        with open(path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def convert_raw_to_feature(self, filename):
        # blocks[idx][height] = [b1, b2, b3]
        blocks = self.load_blocks(filename)
        height_updated = dict()
        for idx_b_type in range(len(self.paths)):
            for height in blocks[idx_b_type]:
                if height in height_updated:
                    # print(f"height {height} has been updated")
                    continue
                # blocks_at_height = list()
                # load all 4 types' blocks
                # print(f"load 4 types' blocks at height {height}")
                total_time = 0
                count = 0
                for type_tmp in range(len(self.paths)):
                    # print(f"load blocks type {type_tmp}")
                    if height in blocks[type_tmp]:
                        # blocks_at_height += blocks[type_tmp][height]
                        for b_tmp in blocks[type_tmp][height]:
                            # print(f"cal total time += {b_tmp['timestamp']}")
                            total_time += float(int(b_tmp['timestamp'], 16))
                            count += 1
                # print(f"4 types' blocks at height {height}: {[each['number'] for each in blocks_at_height]}")
                # update blocks at this height
                time_avg = total_time / count
                for type_tmp in range(len(self.paths)):
                    if height in blocks[type_tmp]:
                        for b_tmp in blocks[type_tmp][height]:
                            b_tmp['timestamp'] = round(float(abs(time_avg - float(int(b_tmp['timestamp'], 16)))), 6)
                height_updated[height] = 1
        self.save_feature(blocks, filename)

    def load_blocks(self, filename):
        # blocks[0=canonical, 1=bc, 2=uncle, 3=forked][height] = block
        blocks = [dict(), dict(), dict(), dict()]
        unique_hashes = set()
        for idx in range(len(self.paths)):
            folder = self.paths[idx][1]
            path = f"{folder}{filename}"
            if not os_path.exists(path):
                continue
            self.done_count += 1
            for line in load_file.load_file_yield_lines(folder, filename):
                b = json.loads(line)
                # remove duplicates
                if b['hash'] in unique_hashes:
                    continue
                else:
                    unique_hashes.add(b['hash'])
                height = b['number']
                if height not in blocks[idx]:
                    blocks[idx][height] = [b]
                else:
                    blocks[idx][height].append(b)
            md5 = self.cal_md5(path)
            print(f"update md5: md5[{self.file_types[idx]}][{filename}] = {md5}")
            self.files_md5[self.file_types[idx]][filename] = md5
        return blocks

    def save_feature(self, blocks, filename):
        # all blocks are from filename's height to +10,000
        for idx_type in range(len(self.paths)):
            load_file.check_dir_exist(f"{self.feature_path}")
            load_file.check_dir_exist(f"{self.feature_path}{self.file_types[idx_type]}")
            content = ""
            for height in blocks[idx_type]:
                for b in blocks[idx_type][height]:
                    data = OrderedDict()
                    data['gasUsed'] = b['gasUsed']
                    data['gasLimit'] = b['gasLimit']
                    data['difficulty'] = b['difficulty']
                    data['number'] = b['number']
                    data['miner'] = b['miner']
                    data['timestamp'] = b['timestamp']
                    data['size'] = b['size']
                    data['txNum'] = b['txNum']
                    data['uncleNum'] = b['uncleNum']
                    data['hash'] = b['hash']
                    content += json.dumps(data) + "\n"
            if content != "":
                save_path = f"{self.feature_path}{self.file_types[idx_type]}/{filename}"
                print(f"saving feature json {save_path}")
                with open(save_path, 'w') as f:
                    # each line is a JSON, not the entire file
                    f.write(content)


if __name__ == '__main__':
    FeatureJsonConverter().run()

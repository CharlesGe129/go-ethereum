import json
import hashlib
import configparser
from analysis_tool_python.util import load_file, cfg

FEATURE_PATH = "./feature_json/"


class FeatureJsonConverter:
    def __init__(self, raw_path, feature_path=FEATURE_PATH):
        # paths[0=canonical, 1=bc, 2=uncle, 3=forked][0=raw_path, 1=json_path]
        self.paths = cfg.load_cfg()
        self.files_md5 = dict()
        self.raw_path = raw_path
        self.feature_path = feature_path
        self.updated_heights = dict()

    def run(self):
        self.load_md5(self.feature_path)
        for filename in load_file.load_path(self.raw_path):
            self.check_md5(filename)

    def load_md5(self, path):
        with open(path, 'r') as f:
            self.files_md5 = json.loads(f.read())

    def dump_md5(self, path):
        with open(path, 'w') as f:
            f.write(json.dumps(self.files_md5))

    @staticmethod
    def cal_md5(path):
        md5_hash = hashlib.md5()
        with open(path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def check_md5(self, filename):
        feature_md5 = self.cal_md5(self.raw_path + filename)
        if filename in self.files_md5[self.file_type] \
                and self.files_md5[self.file_type][filename] == feature_md5:
            return
        else:
            self.convert_raw_to_feature(filename)

    def convert_raw_to_feature(self, filename):
        features = ['height']
        # blocks[idx][height] = [b1, b2, b3]
        blocks = self.load_blocks(filename)
        for idx_b_type in range(len(self.paths)):
            for height in blocks[idx_b_type]:
                # get time diff
                # datetime.strptime('2019-10-01 10:00:00.123', "%Y-%m-%d %H:%M:%S.%f")
                # t1.timestamp() float
                pass

    def load_blocks(self, filename):
        blocks = [dict(), dict(), dict(), dict()]
        for idx in range(len(self.paths)):
            folder = self.paths[idx]
            for line in load_file.load_file_yield_lines(folder, filename):
                b = json.loads(line)
                height = b['height']
                if height not in blocks[idx]:
                    blocks[idx] = [b]
                else:
                    blocks[idx].append(b)
        return blocks

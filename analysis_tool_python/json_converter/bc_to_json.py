import json
import configparser
from analysis_tool_python.util.models.block import Block
from analysis_tool_python.util import load_file, time_format


class BroadcastToJson:
    def __init__(self):
        self.conf_path = '../env.conf'
        config = configparser.ConfigParser()
        config.read(self.conf_path)

        self.bc_path = config.get("broadcast", "raw_path")
        self.save_path = config.get("broadcast", "json_path")
        self.blocks = dict()
        self.unique_block_hashes = dict()

    def start(self):
        for folder in ['ali/', 'aws/']:
            load_file.check_dir_exist(self.save_path)
            path = self.bc_path + folder
            for filename in load_file.load_path(path):
                if not filename.endswith('.txt'):
                    continue
                self.file_to_json(path, filename)
        self.save()

    def file_to_json(self, path, filename):
        for line in load_file.load_file_yield_lines(path, filename):
            if not line.startswith('[20'):
                # Ignore TX lines or empty lines
                continue
            if '{' in line and '}' in line:
                block = self.line_json_ish_to_json(line)
                self.insert_block(block)
            else:
                block = self.line_raw_text_to_json(line)
                self.insert_block(block)

    def insert_block(self, block):
        if block.hash in self.unique_block_hashes:
            return
        else:
            self.unique_block_hashes[block.hash] = 1
        if block.number not in self.blocks:
            self.blocks[block.number] = list()
        self.blocks[block.number].append(block)

    def line_json_ish_to_json(self, line):
        line = '{' + line.split("{")[1].split("}")[0] + '}'
        raw = json.loads(line)
        data = Block()
        data.hash = raw['hash']
        data.parentHash = raw['parentHash']
        data.uncleHash = raw['uncleHash']
        data.receiptHash = raw['receiptHash']
        data.nonce = str(raw['nonce'])
        data.logsBloom = raw['logsBloom']
        data.number = int(raw['number'])
        data.uncles = raw['uncles']
        data.miner = raw['miner']
        data.txNum = int(raw['txNum'])
        data.gasUsed = str(int(raw['gasUsed']))
        data.gasLimit = str(int(raw['gasLimit']))
        data.difficulty = raw['difficulty']
        data.mixDigest = raw['mixDigest']
        data.size = self.format_size(raw['size'])
        data.totalDifficulty = ""
        data.extra = raw['extra']
        data.timestamp = str(int(raw['timestamp']))
        return data

    def line_raw_text_to_json(self, line):
        line += ","
        data = Block()
        data.difficulty = load_file.load_field(line, 'difficulty')
        extra_str = load_file.load_field(line, 'extra')
        if 'timestamp' in extra_str:
            data.extraData = extra_str.split('timestamp')[0]
        else:
            data.extraData = extra_str
        gas_limit_str = load_file.load_field(line, 'gasLimit')
        data.gasLimit = str(int(gas_limit_str)) if gas_limit_str != '' else 0
        gas_used_str = load_file.load_field(line, 'gasUsed')
        data.gasUsed = str(int(gas_used_str)) if gas_used_str != '' else 0
        data.hash = load_file.load_field(line, 'Block Hash')
        data.logsBloom = load_file.load_field(line, 'logsBloom')
        data.miner = load_file.load_field(line, 'miner')
        data.mixHash = ''
        data.nonce = load_file.load_field(line, 'nonce')
        data.number = load_file.load_field(line, 'number')
        data.parentHash = load_file.load_field(line, 'parentHash')
        data.receiptsRoot = load_file.load_field(line, 'receiptHash')
        data.sha3Uncles = ''
        data.size = self.format_size(load_file.load_field(line, 'size'))
        data.stateRoot = ''
        time_str = load_file.load_field(line, 'timestamp')
        t = time_format.load_time_to_utc_unix(time_str, "%Y-%m-%d %H:%M:%S")
        data.timestamp = str(int(t))
        data.totalDifficulty = ''
        data.transactions = ''
        data.transactionsRoot = ''
        data.uncles = [load_file.load_field(line, 'uncleHash')]
        num = load_file.load_field(line, 'uncleNum')
        data.uncleNum = int(num) if num != '' else 0
        num = load_file.load_field(line, 'txNum')
        data.txNum = int(num) if num != '' else 0
        return data

    @staticmethod
    def format_size(size_str):
        if size_str == '':
            return 0
        size_f = float(size_str.split(' ')[0])
        if ' B' in size_str:
            return hex(int(size_f * 8))
        elif ' KiB' in size_str:
            return hex(int(size_f * 8 * 1024))
        elif ' MiB' in size_str:
            return hex(int(size_f * 8 * 1024 * 1024))
        else:
            return hex(int(size_f))

    def save(self):
        contents = dict()
        i = 0
        print(len(self.blocks))
        for height, block_list in self.blocks.items():
            for block in block_list:
                filename = int(int(height) / 10000) * 10000
                if filename not in contents:
                    contents[filename] = ""
                i += 1
                if i % 10000 == 0:
                    print(i)
                contents[filename] += block.to_feature_json() + "\n"
        for height, content in contents.items():
            print(f"saving {self.save_path}{height}.txt")
            with open(f"{self.save_path}{height}.txt", 'w') as f:
                f.write(content)


if __name__ == '__main__':
    BroadcastToJson().start()

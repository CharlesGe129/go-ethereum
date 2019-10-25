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

    def start(self):
        for folder in ['ali/', 'aws/']:
            save_path = self.save_path + folder
            load_file.check_dir_exist(self.save_path)
            load_file.check_dir_exist(save_path)
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
                self.blocks[block.number] = block
            else:
                block = self.line_raw_text_to_json(line)
                self.blocks[block.number] = block

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
        data.gasUsed = int(raw['gasUsed'])
        data.gasLimit = int(raw['gasLimit'])
        data.difficulty = raw['difficulty']
        data.mixDigest = raw['mixDigest']
        data.size = self.format_size(raw['size'])
        data.totalDifficulty = ""
        data.extra = raw['extra']
        data.timestamp = hex(int(raw['timestamp']))
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
        data.gasLimit = hex(int(gas_limit_str)) if gas_limit_str != '' else 0
        gas_used_str = load_file.load_field(line, 'gasUsed')
        data.gasUsed = hex(int(gas_used_str)) if gas_used_str != '' else 0
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
        data.timestamp = hex(int(t))
        data.totalDifficulty = ''
        data.transactions = ''
        data.transactionsRoot = ''
        data.uncles = [load_file.load_field(line, 'uncleHash')]
        data.uncleNum = load_file.load_field(line, 'uncleNum')
        data.txNum = load_file.load_field(line, 'txNum')
        return data

    def file_to_json_backup(self, path, filename, save_path):
        content = ""
        for line in load_file.load_file_yield_lines(path, filename):
            if line.startswith('0x') or line.startswith("tx"):
                # tx line
                continue
            line += ","
            data = dict()
            data['difficulty'] = ''
            extra_str = load_file.load_field(line, 'extra')
            if 'timestamp' in extra_str:
                data['extraData'] = extra_str.split('timestamp')[0]
            else:
                data['extraData'] = extra_str
            gas_limit_str = load_file.load_field(line, 'gasLimit')
            data['gasLimit'] = hex(int(gas_limit_str)) if gas_limit_str != '' else 0
            gas_used_str = load_file.load_field(line, 'gasUsed')
            data['gasUsed'] = hex(int(gas_used_str)) if gas_used_str != '' else 0
            data['hash'] = load_file.load_field(line, 'Block Hash')
            data['logsBloom'] = load_file.load_field(line, 'logsBloom')
            data['miner'] = load_file.load_field(line, 'miner')
            data['mixHash'] = ''
            data['nonce'] = load_file.load_field(line, 'nonce')
            data['number'] = load_file.load_field(line, 'number')
            data['parentHash'] = load_file.load_field(line, 'parentHash')
            data['receiptsRoot'] = load_file.load_field(line, 'receiptHash')
            data['sha3Uncles'] = ''
            data['size'] = self.format_size(load_file.load_field(line, 'size'))
            data['stateRoot'] = ''
            time_str = load_file.load_field(line, 'timestamp')
            data['timestamp'] = time_format.load_time_to_utc_unix(time_str, "%Y-%m-%d %H:%M:%S")
            data['totalDifficulty'] = ''
            data['transactions'] = ''
            data['transactionsRoot'] = ''
            data['uncles'] = [load_file.load_field(line, 'uncleHash')]
            data['uncleNum'] = load_file.load_field(line, 'uncleNum')
            data['txNum'] = load_file.load_field(line, 'txNum')
            content += json.dumps(data) + '\n'
        with open(save_path + filename.replace('.txt', '.json'), 'w') as f:
            # each line is a JSON, not the entire file
            f.write(content)

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
        for height, block in self.blocks.items():
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

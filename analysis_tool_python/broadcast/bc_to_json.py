import time
import json
from datetime import datetime
from util import load_file, time_format


class BroadcastToJson:
    def __init__(self):
        self.bc_path = '../../records/blocks/'
        self.save_path = '../../records/block_json/'

    def start(self):
        for folder in ['ali/', 'aws/']:
            save_path = self.save_path + folder
            load_file.check_dir_exist(self.save_path)
            load_file.check_dir_exist(save_path)
            path = self.bc_path + folder
            for filename in load_file.load_path(path):
                if not filename.endswith('.txt'):
                    continue
                self.file_to_json(path, filename, save_path)

    def file_to_json(self, path, filename, save_path):
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


if __name__ == '__main__':
    BroadcastToJson().start()

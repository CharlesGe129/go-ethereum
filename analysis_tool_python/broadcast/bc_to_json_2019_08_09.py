import time
import json
from datetime import datetime
from analysis_tool_python.util.models.block import Block
from util import load_file, time_format


class BroadcastToJson:
    def __init__(self):
        self.bc_path = '../../records/blocks/'
        self.save_path = '../../records/block_json/'

    def start(self):
        for folder in ['ali_2019_08_09/', 'aws_2019_08_09/']:
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
            if not line.startswith('[20'):
                # Ignore TX lines or empty lines
                continue
            # line += ","
            # [2019-08-09 07:04:40.539345609 +0800 CST m=+193.301725712] {"hash":"0x1ca6af364f156a5c4e8f48a59b4f89d84cdf071a6f47f7e138c78539ffa6f849",
            # "parentHash":"0x2cefce21cfb17a4c5e1086d18bff5b79ba41370a26a6e676695e9c7f285f79b2",
            # "uncleHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
            # "receiptHash":"0x763422e391079d0db0b18f40ee0bba9a7347568b18328ff97ed87c1342d27ce6",
            # "nonce":9070223003597812241,
            # "logsBloom":"00201a80502400000013047000484010206080a040800024010040001030000801280040209100040230310000a0050058000000240000000000118001000020090110011022050040c6d01801000000034000040200005000000054005100000000160c0a0010902104200001082904100098400802082000000834410000000000002000440000120100850040041001800ac00c00800011114080011080080008000400031000000002900241888040000a0400538000008001020100301040000a0259848480000030000900260004008084001000000808009001146003300004001023001808810045400400c168040000000020803400000808100020",
            # "number":"8274014",
            # "miner":"0x829BD824B016326A401d083B33D092293333A830",
            # "uncles":null,
            # "txNum":53,
            # "gasUsed":3950579,
            # "gasLimit":8007840,
            # "difficulty":"2204917006018504",
            # "root":"0x883249a57eba8296ff18de315529a9e9a15435882df0e6aece6131ae43bd8b88",
            # "mixDigest":"0x039c897e39b5753a76f0dbe9ac846b869be116af1eedd9edaed3095fbe04438e",
            # "size":"11.03 KiB",
            # "totalDifficulty":"\u003cnil\u003e",
            # "extra":"7070796520e4b883e5bda9e7a59ee4bb99e9b1bc",
            # "timestamp":1564786049}
            print('path file name: ', path, filename)
            print('original line: ' + line)
            line = line.split('] ')[1]
            print('split line: ' + line)
            tmp_json = json.loads(line)
            tmp_json['nonce'] = str(tmp_json['nonce'])
            line = json.dumps(tmp_json)
            # test_line_json = json.loads(line)
            # # print('test line json:' + test_line_json)
            # print(test_line_json['hash'])
            # print(test_line_json)
            # return

            # data = Block()
            # data.difficulty = load_file.load_field(line, 'difficulty')
            # extra_str = load_file.load_field(line, 'extra')
            # if 'timestamp' in extra_str:
            #     data.extraData = extra_str.split('timestamp')[0]
            # else:
            #     data.extraData = extra_str
            # gas_limit_str = load_file.load_field(line, 'gasLimit')
            # data.gasLimit = hex(int(gas_limit_str)) if gas_limit_str != '' else 0
            # gas_used_str = load_file.load_field(line, 'gasUsed')
            # data.gasUsed = hex(int(gas_used_str)) if gas_used_str != '' else 0
            # data.hash = load_file.load_field(line, 'Block Hash')
            # data.logsBloom = load_file.load_field(line, 'logsBloom')
            # data.miner = load_file.load_field(line, 'miner')
            # data.mixHash = ''
            # data.nonce = load_file.load_field(line, 'nonce')
            # data.number = load_file.load_field(line, 'number')
            # data.parentHash = load_file.load_field(line, 'parentHash')
            # data.receiptsRoot = load_file.load_field(line, 'receiptHash')
            # data.sha3Uncles = ''
            # data.size = self.format_size(load_file.load_field(line, 'size'))
            # data.stateRoot = ''
            # time_str = load_file.load_field(line, 'timestamp')
            # data.timestamp = time_format.load_time_to_utc_unix(time_str, "%Y-%m-%d %H:%M:%S")
            # data.totalDifficulty = ''
            # data.transactions = ''
            # data.transactionsRoot = ''
            # data.uncles = [load_file.load_field(line, 'uncleHash')]
            # data.uncleNum = load_file.load_field(line, 'uncleNum')
            # data.txNum = load_file.load_field(line, 'txNum')
            # content += data.to_json() + '\n'
            content += line + '\n'
        with open(save_path + filename.replace('.txt', '.json'), 'w') as f:
            # each line is a JSON, not the entire file
            f.write(content + '\n')
        #return

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


if __name__ == '__main__':
    BroadcastToJson().start()

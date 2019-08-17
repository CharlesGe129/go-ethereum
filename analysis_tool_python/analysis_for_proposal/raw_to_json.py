import json
import configparser
from analysis_tool_python.util import load_file
from analysis_tool_python.util.models.block import Block


class ApiToJson:
    def __init__(self):
        self.conf_path = '../env.conf'
        config = configparser.ConfigParser()
        config.read(self.conf_path)
        # [0]=raw_path, [1]=json_path
        self.uncle_paths = [config.get("uncle", "raw_path"), config.get("uncle", "json_path")]
        self.canonical_paths = [config.get("canonical", "raw_path"), config.get("canonical", "json_path")]
        self.paths = [self.uncle_paths, self.canonical_paths]

    def start(self):
        if self.check_json_converted():
            return
        for paths in self.paths:
            load_file.check_dir_exist(paths[1])
            for filename in load_file.load_path(paths[0]):
                if not filename.endswith('.txt'):
                    continue
                self.file_to_json(paths[0], filename, paths[1])

    def check_json_converted(self):
        # TODO: check if files in two dir are the same
        return False

    @staticmethod
    def file_to_json(path, filename, save_path):
        block_str = ""
        for line in load_file.load_file_yield_lines(path, filename):
            if not line.startswith('{'):
                # Ignore invalid lines
                continue
            content = json.loads(line)
            data = Block()
            data.difficulty = load_file.load_field_from_dict(content, "difficulty", data.difficulty)
            data.extraData = load_file.load_field_from_dict(content, "extraData", data.extraData)
            data.gasLimit = int(load_file.load_field_from_dict(content, "gasLimit", data.gasLimit), 16)
            data.gasUsed = int(load_file.load_field_from_dict(content, "gasUsed", data.gasUsed), 16)
            data.hash = load_file.load_field_from_dict(content, "hash", data.hash)
            data.logsBloom = load_file.load_field_from_dict(content, "logsBloom", data.logsBloom)
            data.nonce = int(load_file.load_field_from_dict(content, "nonce", data.nonce), 16)
            data.number = int(load_file.load_field_from_dict(content, "number", data.number), 16)
            data.size = int(load_file.load_field_from_dict(content, "size", data.size), 16)
            data.timestamp = int(load_file.load_field_from_dict(content, "timestamp", data.timestamp), 16)
            data.miner = load_file.load_field_from_dict(content, "miner", data.miner)
            data.mixHash = load_file.load_field_from_dict(content, "mixHash", data.mixHash)
            data.parentHash = load_file.load_field_from_dict(content, "parentHash", data.parentHash)
            data.receiptsRoot = load_file.load_field_from_dict(content, "receiptsRoot", data.receiptsRoot)
            data.sha3Uncles = load_file.load_field_from_dict(content, "sha3Uncles", data.sha3Uncles)
            data.stateRoot = load_file.load_field_from_dict(content, "stateRoot", data.stateRoot)
            data.totalDifficulty = load_file.load_field_from_dict(content, "totalDifficulty", data.totalDifficulty)
            data.transactionsRoot = load_file.load_field_from_dict(content, "transactionsRoot", data.transactionsRoot)
            data.transactions = load_file.load_field_from_dict(content, "transactions", data.transactions)
            data.txNum = len(data.transactions)
            data.uncles = load_file.load_field_from_dict(content, "uncles", data.uncles)
            data.uncleNum = len(data.uncles)
            block_str += data.to_json() + '\n'
        with open(save_path + filename.replace('.txt', '.json'), 'w') as f:
            # each line is a JSON, not the entire file
            f.write(block_str)


if __name__ == "__main__":
    ApiToJson().start()

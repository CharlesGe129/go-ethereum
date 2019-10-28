import os
import json
import time
import configparser
from datetime import datetime
from analysis_tool_python.util.models.block import Block
from analysis_tool_python.util import load_file


class ForkedToJson:
    def __init__(self):
        self.conf_path = '../env.conf'
        config = configparser.ConfigParser()
        config.read(self.conf_path)

        self.raw_path = config.get("forked", "raw_path")
        self.json_path = config.get("forked", "json_path")
        self.blocks = dict()

    def start(self):
        if not os.path.isdir(self.json_path):
            os.mkdir(self.json_path)
        for filename in load_file.load_path(self.raw_path):
            print(f"loading {filename}")
            self.convert_file(filename)
        self.save()

    def convert_file(self, filename):
        ori_path = self.raw_path + filename
        save_path = self.json_path + filename
        with open(ori_path) as f:
            lines = f.readlines()
        for line in lines:
            block = self.line_to_json(line)
            self.blocks[block.number] = block

    def line_to_json(self, line):
        block = Block()
        block.number = int(line.split('blockHeight=')[1].split(',')[0])
        time_unformated = line.split('timeStampUnformated=')[1].split(',')[0]
        t = datetime.strptime(time_unformated[:-5], '%b-%d-%Y %I:%M:%S %p')
        unix_time = time.mktime(t.timetuple())
        block.timestamp = str(int(unix_time))
        block.reorgDepth = line.split('reorgDepth=')[1].split(',')[0] if 'reorgDepth' in line else ''
        block.miner = line.split('minerHash=')[1].split(',')[0]
        block.minerName = line.split('miner=')[1].split(',')[0]
        block.mineTime = line.split('mineTime=')[1].split(',')[0]
        block.reward = line.split('reward=')[1].split(',')[0]
        block.uncleReward = line.split('uncleReward=')[1].split(',')[0]
        block.difficulty = self.str_replace_comma(line.split('difficulty=')[1].split(',totalDifficulty')[0])
        block.totalDifficulty = self.str_replace_comma(line.split('totalDifficulty=')[1].split(',size')[0])
        block.size = str(int(self.str_replace_comma(line.split('size=')[1].split(',gasUsed')[0])))
        block.gasUsed = str(int(self.str_replace_comma(line.split('gasUsed=')[1].split(',gasLimit')[0])))
        block.gasLimit = str(int(self.str_replace_comma(line.split('gasLimit=')[1].split(',extraData')[0])))
        block.extraData = line.split('extraData=')[1].split(',')[0]
        block.hash = line.split('hash=')[1].split(',')[0]
        block.parentHash = line.split('parentHash=')[1].split(',')[0]
        block.sha3Uncles = line.split('sha3Uncles=')[1].split(',')[0]
        block.nonce = line.split('nonce=')[1].strip('\n')
        return block

    @staticmethod
    def str_replace_comma(data):
        return data.replace(',', '')

    def save(self):
        contents = dict()
        for height, block in self.blocks.items():
            filename = int(height / 10000) * 10000
            if filename not in contents:
                contents[filename] = ""
            contents[filename] += block.to_feature_json() + "\n"
        for height, content in contents.items():
            print(f"saving {self.json_path}{height}.txt")
            with open(f"{self.json_path}{height}.txt", 'w') as f:
                f.write(content)


if __name__ == '__main__':
    ForkedToJson().start()

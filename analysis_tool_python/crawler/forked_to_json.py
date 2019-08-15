import os
import json
import time
from datetime import datetime
from analysis_tool_python.util.models.block import Block
from util import load_file

PATH = '../crawler/forked/'
JSON_PATH = '../crawler/forked_json/'


def start():
    if not os.path.isdir(JSON_PATH):
        os.mkdir(JSON_PATH)
    for filename in load_file.load_path(PATH):
        print(f"converting {filename}")
        convert_file(filename)


def convert_file(filename):
    ori_path = PATH + filename
    save_path = JSON_PATH + filename
    with open(ori_path) as f:
        lines = f.readlines()
    content = ''
    for line in lines:
        content += line_to_json(line)
    with open(save_path, 'w') as f:
        f.write(content)


def line_to_json(line):
    block = Block()
    block.number = int(line.split('blockHeight=')[1].split(',')[0])
    time_unformated = line.split('timeStampUnformated=')[1].split(',')[0]
    t = datetime.strptime(time_unformated[:-5], '%b-%d-%Y %I:%M:%S %p')
    unix_time = time.mktime(t.timetuple())
    block.timestamp = int(unix_time)
    block.reorgDepth = line.split('reorgDepth=')[1].split(',')[0] if 'reorgDepth' in line else ''
    block.miner = line.split('minerHash=')[1].split(',')[0]
    block.minerName = line.split('miner=')[1].split(',')[0]
    block.mineTime = line.split('mineTime=')[1].split(',')[0]
    block.reward = line.split('reward=')[1].split(',')[0]
    block.uncleReward = line.split('uncleReward=')[1].split(',')[0]
    block.difficulty = str_replace_comma(line.split('difficulty=')[1].split(',totalDifficulty')[0])
    block.totalDifficulty = str_replace_comma(line.split('totalDifficulty=')[1].split(',size')[0])
    block.size = int(str_replace_comma(line.split('size=')[1].split(',gasUsed')[0]))
    block.gasUsed = int(str_replace_comma(line.split('gasUsed=')[1].split(',gasLimit')[0]))
    block.gasLimit = int(str_replace_comma(line.split('gasLimit=')[1].split(',extraData')[0]))
    block.extraData = line.split('extraData=')[1].split(',')[0]
    block.hash = line.split('hash=')[1].split(',')[0]
    block.parentHash = line.split('parentHash=')[1].split(',')[0]
    block.sha3Uncles = line.split('sha3Uncles=')[1].split(',')[0]
    block.nonce = line.split('nonce=')[1].strip('\n')
    return block.to_json() + '\n'


def str_replace_comma(data):
    return data.replace(',', '')


if __name__ == '__main__':
    start()

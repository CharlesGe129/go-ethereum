import os
import json
import time
from datetime import datetime

PATH = '../crawler/forked/'
JSON_PATH = '../crawler/forked_json/'


def start():
    if not os.path.isdir(JSON_PATH):
        os.mkdir(JSON_PATH)
    for filename in os.listdir(PATH):
        if not filename.endswith(".txt"):
            continue
        print(f"converting {filename}")
        load_file(filename)


def load_file(filename):
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
    info = dict()
    info['number'] = hex(int(line.split('blockHeight=')[1].split(',')[0]))
    time_unformated = line.split('timeStampUnformated=')[1].split(',')[0]
    t = datetime.strptime(time_unformated[:-5], '%b-%d-%Y %I:%M:%S %p')
    unix_time = time.mktime(t.timetuple())
    info['timestamp'] = hex(int(unix_time))
    info['reorgDepth'] = line.split('reorgDepth=')[1].split(',')[0] if 'reorgDepth' in line else ''
    info['miner'] = line.split('minerHash=')[1].split(',')[0]
    info['minerName'] = line.split('miner=')[1].split(',')[0]
    info['mineTime'] = line.split('mineTime=')[1].split(',')[0]
    info['reward'] = line.split('reward=')[1].split(',')[0]
    info['uncleReward'] = line.split('uncleReward=')[1].split(',')[0]
    info['difficulty'] = str_to_hex(line.split('difficulty=')[1].split(',totalDifficulty')[0])
    info['totalDifficulty'] = str_to_hex(line.split('totalDifficulty=')[1].split(',size')[0])
    info['size'] = str_to_hex(line.split('size=')[1].split(',gasUsed')[0])
    info['gasUsed'] = str_to_hex(line.split('gasUsed=')[1].split(',gasLimit')[0])
    info['gasLimit'] = str_to_hex(line.split('gasLimit=')[1].split(',extraData')[0])
    info['extraData'] = line.split('extraData=')[1].split(',')[0]
    info['hash'] = line.split('hash=')[1].split(',')[0]
    info['parentHash'] = line.split('parentHash=')[1].split(',')[0]
    info['sha3Uncles'] = line.split('sha3Uncles=')[1].split(',')[0]
    info['nonce'] = line.split('nonce=')[1].strip('\n')
    return json.dumps(info) + '\n'


def str_to_hex(data):
    return hex(int(data.replace(',', '')))


if __name__ == '__main__':
    start()

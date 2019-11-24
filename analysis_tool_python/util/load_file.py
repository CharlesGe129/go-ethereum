import os
import json
from analysis_tool_python.util.models.block import Block


def get_file_lines(path, filename, mode='r'):
    print('loading ' + path + filename)
    with open(path + filename, mode) as f:
        return f.readlines()


def load_file_yield_lines(path, filename, mode='r'):
    print('loading ' + path + filename)
    with open(path + filename, mode) as f:
        while True:
            line = f.readline()
            if not line:
                break
            elif line == '\n':
                continue
            yield line.strip("\n")


def load_path(path):
    for filename in sorted(os.listdir(path)):
        if "ds_store" in filename.lower():
            continue
        yield filename


def load_field(line, field):
    if field in line:
        return line.split(f'{field}=')[1].split(',')[0]
    else:
        return ''


def load_field_from_dict(data, field, default=''):
    if field in data:
        return data[field]
    else:
        return default


def check_dir_exist(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def load_json_file_yield_block(path, filename):
    for line in load_file_yield_lines(path, filename):
        data = json.loads(line)
        block = Block()
        block.gasUsed = load_field_from_dict(data, 'gasUsed')
        block.gasLimit = load_field_from_dict(data, 'gasLimit')
        block.difficulty = load_field_from_dict(data, 'difficulty')
        block.number = load_field_from_dict(data, 'number')
        block.miner = load_field_from_dict(data, 'miner')
        block.timestamp = load_field_from_dict(data, 'timestamp')
        block.size = load_field_from_dict(data, 'size')
        block.txNum = load_field_from_dict(data, 'txNum')
        block.uncleNum = load_field_from_dict(data, 'uncleNum')
        block.hash = load_field_from_dict(data, 'hash')
        block.parentHash = load_field_from_dict(data, 'parentHash')
        yield block

import os


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

import os
from datetime import datetime
# from analysis_tool_python.backup import backup
from backup import backup

RECORD_PATH = '../records'


def clean_tx(file_path):
    u = dict()
    rs = ''
    date_ok = True
    filename = file_path.split('/')[-1]
    last_date = f'[{filename.split("_")[0]} {filename.split("_")[1].split(".")[0]}:00:00.015303602 +0000 UTC m=+196751.022868978]'
    with open(file_path, 'r') as f:
        print(f"Cleaning {file_path}")
        while True:
            line = f.readline()
            if not line:
                break
            if '0x' not in line:
                continue
            h = line.split("Hash=")[1].split(", ")[0] if "Hash=" in line else line.split(' ')[-1].strip('\n')
            if h not in u:
                this_date_ok, line, last_date = try_parse_date(line, last_date)
                date_ok = date_ok & this_date_ok
                u[h] = 1
                rs += line
            else:
                continue
    if not date_ok:
        return
    with open(f"{file_path.split('/txs/')[0]}/txs/cleaned/{file_path.split('/txs/')[1]}", 'w') as f:
        f.write(rs)
    backup(file_path, f"{file_path.split('/txs/')[0]}/txs/backup/{file_path.split('/txs/')[1]}")


def try_parse_date(line, last_date):
    created_at = line.split(" m=")[0].strip('[')
    time = created_at.split('.')[0] + ' ' + ' '.join(created_at.split(' ')[2:])
    try:
        datetime.strptime(time, '%Y-%m-%d %H:%M:%S %z %Z').replace(tzinfo=None)
        last_date = line.split(' Hash=')[0]
        return True, line, last_date
    except:
        try:
            # print(f"Try date format at: {line}")
            line = last_date + " Hash=" + line.split(" Hash=")[1]
            # print(f"New line: {line}")
            created_at = line.split(" m=")[0].strip('[')
            time = created_at.split('.')[0] + ' ' + ' '.join(created_at.split(' ')[2:])
            datetime.strptime(time, '%Y-%m-%d %H:%M:%S %z %Z').replace(tzinfo=None)
            return True, line, last_date
        except:
            print(f"Date format goes wrong at: {line}")
            return False, line, last_date


def clean_txs():
    for f in os.listdir(RECORD_PATH + '/txs'):
        if not f.endswith('.txt'):
            continue
        try:
            file_path = RECORD_PATH + '/txs/' + f
            clean_tx(file_path)
        except Exception as e:
            print(f"file {f} went wrong: {e}")


if __name__ == '__main__':
    clean_txs()

import pickle
import statistics
from analysis_tool_python.util.time_format import utc_unix_to_date
from analysis_tool_python.util.cfg import load_cfg
from analysis_tool_python.util.load_file import *


class CanonicalStatistics:
    def __init__(self, cfg_path="../env.conf"):
        self.paths = load_cfg(cfg_path)  # [cano, bc, uncle, fork][1=json]
        self.blocks_by_height = dict()  # [height][hash] = block
        self.blocks_by_date = dict()  # [20190910] = list()

        self.mean_daily = dict()  # [field][date] = mean
        self.mean_height = dict()  # [field][height] = mean

        self.total_canonical = 0
        self.total_blocks = 0
        self.valid_count = dict()  # [field][0=total, 1=canonical] = num

        self.miner_stats = dict()  # see func cal_miner_stats()
        self.miner_canonical_num = dict()  # [miner][0=cano, 1=non_cano] = num

        self.differences = dict()  # [field][0=cur-total_mean, 1=cur-mean_height, 2=cur-mean_daily][0=cano, 1=non_cano] = list()

        self.overall_stats = dict()  # [field][min, max, std, mean]
        self.organized_data = dict()  # [field][diff_mean_total, diff_mean_height, diff_mean_date][idx] = {"lower", "upper", "data", "cano_num"}

    def start(self):
        self.load_blocks()
        self.prepare_extra_fields()
        self.get_blocks_daily()
        self.cal_miner_stats()

        field_and_funcs = [
            ["size", lambda block: int(block.size, 16) if block.size.startswith("0x") else int(block.size)],
            ["gasUsed", lambda block: int(block.gasUsed)],
            ["gasLimit", lambda block: int(block.gasLimit)],
            ["uncleNum", lambda block: int(block.uncleNum)],
            ["difficulty",
             lambda block: -1 if block.difficulty == "" else (int(block.difficulty, 16)
                                                              if block.difficulty.startswith("0x")
                                                              else int(block.difficulty))],
            ["mineTime", lambda block: int(block.mineTime)],
            ["timeDiff", lambda block: float(block.timeDiff)],
            ["gasPercent",
             lambda block: float(block.gasUsed) / float(block.gasLimit) if float(block.gasLimit) != 0 else -1],
        ]

        self.cal_mean_and_overall(field_and_funcs)

        self.cal_differences(field_and_funcs)

        self.organize_differences(10)

        self.print_stats()

    # 从4个path中读取4种block
    def load_blocks(self):
        # cano
        self.load_blocks_in_path(self.paths[0][1], True)

        # bc, uncle, fork
        for paths in self.paths[1:]:
            self.load_blocks_in_path(paths[1], False)

    # 读取路径下所有block json文件，并记录block是否为canonical
    def load_blocks_in_path(self, json_path, is_canonical):
        for filename in load_path(json_path):
            for b in load_json_file_yield_block(json_path, filename):
                height = b.number
                hash_value = b.hash
                if height not in self.blocks_by_height:
                    self.blocks_by_height[height] = dict()
                if hash_value not in self.blocks_by_height[height]:
                    if is_canonical:
                        b.is_canonical = True
                        self.total_canonical += 1
                    else:
                        b.is_canonical = False
                    self.blocks_by_height[height][hash_value] = b
                    self.total_blocks += 1
                else:
                    self.blocks_by_height[height][hash_value].amend_missing_fields(b)

    # 为每个block计算mine time和time diff
    def prepare_extra_fields(self):
        print("preparing extra fields")
        for height, blocks_height in self.blocks_by_height.items():
            time_diff_list = [int(b.timestamp) for b in blocks_height.values()]
            time_diff_mean = statistics.mean(time_diff_list)

            for hash_value, b in blocks_height.items():
                # mine time
                parent_num = b.number - 1
                parent_hash = b.parentHash
                if parent_num in self.blocks_by_height and parent_hash in self.blocks_by_height[parent_num]:
                    b.mineTime = str(int(b.timestamp) - int(self.blocks_by_height[parent_num][parent_hash].timestamp))
                else:
                    b.mineTime = "-1"

                # time diff
                b.timeDiff = str(int(b.timestamp) - time_diff_mean)

    # 遍历所有block，先计算2种之后统计需要用到的mean(mean_date, mean_height), 再计算所有field的全局min, max, mean, std
    def cal_mean_and_overall(self, field_and_funcs):
        # field_and_funcs[field=0, get_field_func=1]
        print("calculating mean")
        value_total = dict()  # [field] = list()
        for field_and_func in field_and_funcs:
            field = field_and_func[0]
            value_total[field] = list()
            self.mean_daily[field] = dict()
            self.mean_height[field] = dict()
            self.valid_count[field] = [0, 0]

        # mean daily
        print("calculating mean daily")
        total = len(self.blocks_by_date)
        i = 0
        for date, block_list in self.blocks_by_date.items():
            i += 1
            if i % 10000 == 0:
                print(f"calculate mean daily, process {round(i / total * 100, 3)}%")
            for field_and_func in field_and_funcs:
                field = field_and_func[0]
                get_func = field_and_func[1]
                value_list = list()
                for b in block_list:
                    val = get_func(b)
                    if val >= 0:
                        value_list.append(val)
                if value_list:
                    self.mean_daily[field][date] = statistics.mean(value_list)

        # mean height
        print("calculating mean height")
        total = len(self.blocks_by_height)
        i = 0
        for height, blocks_by_hash in self.blocks_by_height.items():
            i += 1
            if i % 10000 == 0:
                print(f"calculate mean height, process {round(i / total * 100, 3)}%")
            for field_and_func in field_and_funcs:
                field = field_and_func[0]
                get_func = field_and_func[1]
                value_list = list()
                for b in blocks_by_hash.values():
                    val = get_func(b)
                    if val >= 0:
                        value_list.append(val)
                        self.valid_count[field][0] += 1
                        if b.is_canonical:
                            self.valid_count[field][1] += 1
                value_total[field] += value_list
                if value_list:
                    self.mean_height[field][height] = statistics.mean(value_list)

        print("calculating overall stats")
        # mean total
        for field_and_func in field_and_funcs:
            field = field_and_func[0]
            stats = dict()
            stats["min"] = min(value_total[field])
            stats["max"] = max(value_total[field])
            stats["mean"] = statistics.mean(value_total[field])
            stats["std"] = statistics.stdev(value_total[field])
            self.overall_stats[field] = stats

    # 把所有block按照日期存成dict
    def get_blocks_daily(self):
        print("converting blocks by date")
        blocks_daily = dict()  # [20190910] = list()
        for blocks_height in self.blocks_by_height.values():
            for b in blocks_height.values():
                time_str = utc_unix_to_date(b.timestamp)
                if time_str in blocks_daily:
                    blocks_daily[time_str].append(b)
                else:
                    blocks_daily[time_str] = [b]
        self.blocks_by_date = blocks_daily

    # 计算miner相关的4个统计数据
    def cal_miner_stats(self):
        print("calculating miner stats")
        miner_cano_num = dict()
        miner_cano_percent = dict()
        miner_cano_total_cano_percent = dict()
        miner_cano_total_block_percent = dict()

        for miner, numbers in self.miner_canonical_num:
            c = numbers[0]
            nc = numbers[1]
            miner_cano_num[miner] = c
            miner_cano_percent[miner] = c / (c + nc)
            miner_cano_total_cano_percent[miner] = c / self.total_canonical
            miner_cano_total_block_percent[miner] = c / self.total_blocks

        self.miner_stats = [miner_cano_num, miner_cano_percent, miner_cano_total_cano_percent,
                            miner_cano_total_block_percent]

    # 对每个字段，统计所有block的3种differences(cur-mean_total, cur-mean_date, cur-mean_height)
    def cal_differences(self, field_and_funcs):
        # field_and_funcs[field=0, get_field_func=1]
        for field_and_func in field_and_funcs:
            field = field_and_func[0]
            get_func = field_and_func[1]
            differences = [[list(), list()], [list(), list()], [list(), list()]]
            cano_num, non_cano_num = 0, 0
            for date, block_list in self.blocks_by_date.items():
                for b in block_list:
                    val = get_func(b)
                    if val < 0:
                        continue
                    if b.is_canonical:
                        cano_num += 1
                        differences[0][0].append(val - self.overall_stats[field]['mean'])
                        differences[1][0].append(val - self.mean_height[field][b.number])
                        differences[2][0].append(val - self.mean_daily[field][date])
                    else:
                        non_cano_num += 1
                        differences[0][1].append(val - self.overall_stats[field]['mean'])
                        differences[1][1].append(val - self.mean_height[field][b.number])
                        differences[2][1].append(val - self.mean_daily[field][date])
            self.differences[field] = differences
            print(f"cal_differences, field={field}, cano_num={cano_num}, non_cano_num={non_cano_num}")

    # 将所有的differences数据进行分片，默认10片
    def organize_differences(self, piece_num):
        print(f"organizing differences")
        for field, differences in self.differences.items():
            data = [list(), list(), list()]
            for i in range(len(differences)):
                diff_list = differences[i]
                data[i] = self.organize_diff(diff_list, piece_num)
            self.organized_data[field] = data

    # 对1个list数据进行分片，先计算每一片的上限和下限，然后将所有数据放在不同的片中
    @staticmethod
    def organize_diff(diff_lists, piece_num):
        # diff_lists[0=cano, 1=non_cano] = list()
        diff_total = diff_lists[0] + diff_lists[1]
        upper_total = int(max(diff_total))
        lower_total = int(min(diff_total))
        middle_total = (upper_total + lower_total) / 2

        diff_in_pieces = list()  # {}
        piece = (upper_total - lower_total) / piece_num
        for i in range(piece_num):
            diff_in_pieces.append({
                "lower": lower_total + i * piece,
                "upper": lower_total + (i + 1) * piece,
                "data": list(),
                "cano_num": 0,
            })
        for i in range(2):
            diff_list = diff_lists[i]
            is_canonical = 1 if i == 0 else 0
            for diff in diff_list:
                if diff < middle_total:
                    # starts with [0]
                    for each in diff_in_pieces:
                        if diff < each['upper']:
                            each['data'].append(diff)
                            each['cano_num'] += is_canonical
                            break
                else:
                    # starts with [-1]
                    i = len(diff_in_pieces)
                    while i > 0:
                        i -= 1
                        each = diff_in_pieces[i]
                        if diff >= each['lower']:
                            each['data'].append(diff)
                            each['cano_num'] += is_canonical
                            break
        return diff_in_pieces

    # 打印一些基本统计信息
    def print_stats(self):
        diff_names = ["diff_mean_total", "diff_mean_height", "diff_mean_date"]
        for field, diff_lists in self.organized_data.items():
            print("")
            for i in range(len(diff_lists)):
                diff_list = diff_lists[i]
                idx = -1
                for piece in diff_list:
                    idx += 1
                    print(f"{field}[{diff_names[i]}][{idx}]:lower={piece['lower']}, upper={piece['upper']}, "
                          f"len={len(piece['data'])}, cano_percent={round(piece['cano_num'] / self.valid_count[field][1] * 100, 2)}%, "
                          f"non_cano_percent={round((len(piece['data']) - piece['cano_num']) / (self.valid_count[field][0] - self.valid_count[field][1]) * 100, 2)}")

    # 保存成pickle。如果with_blocks=False，会清空所有blocks数据
    def save_pickle(self, with_blocks=False):
        prefix = "cano_stats_"
        pickle.dump(self.mean_daily, open(prefix + "mean_daily" + ".p", 'wb'))
        pickle.dump(self.mean_height, open(prefix + "mean_height" + ".p", 'wb'))

        pickle.dump(self.total_canonical, open(prefix + "total_canonical" + ".p", 'wb'))
        pickle.dump(self.total_blocks, open(prefix + "total_blocks" + ".p", 'wb'))
        pickle.dump(self.valid_count, open(prefix + "valid_count" + ".p", 'wb'))

        pickle.dump(self.miner_stats, open(prefix + "miner_stats" + ".p", 'wb'))
        pickle.dump(self.miner_canonical_num, open(prefix + "miner_canonical_num" + ".p", 'wb'))

        pickle.dump(self.differences, open(prefix + "differences" + ".p", 'wb'))

        pickle.dump(self.overall_stats, open(prefix + "overall_stats" + ".p", 'wb'))
        pickle.dump(self.organized_data, open(prefix + "organized_data" + ".p", 'wb'))

        if with_blocks:
            pickle.dump(self.blocks_by_height, open(prefix + "blocks_by_height" + ".p", 'wb'))
            pickle.dump(self.blocks_by_date, open(prefix + "blocks_by_date" + ".p", 'wb'))

    def load_pickle(self):
        prefix = "cano_stats_"
        self.mean_daily = pickle.load(open(prefix + "mean_daily" + ".p", 'rb'))
        self.mean_height = pickle.load(open(prefix + "mean_height" + ".p", 'rb'))

        self.total_canonical = pickle.load(open(prefix + "total_canonical" + ".p", 'rb'))
        self.total_blocks = pickle.load(open(prefix + "total_blocks" + ".p", 'rb'))
        self.valid_count = pickle.load(open(prefix + "valid_count" + ".p", 'rb'))

        self.miner_stats = pickle.load(open(prefix + "miner_stats" + ".p", 'rb'))
        self.miner_canonical_num = pickle.load(open(prefix + "miner_canonical_num" + ".p", 'rb'))

        self.differences = pickle.load(open(prefix + "differences" + ".p", 'rb'))

        self.overall_stats = pickle.load(open(prefix + "overall_stats" + ".p", 'rb'))
        self.organized_data = pickle.load(open(prefix + "organized_data" + ".p", 'rb'))

        if os.path.exists(prefix + "blocks_by_height.p"):
            pickle.dump(self.blocks_by_height, open(prefix + "blocks_by_height" + ".p", 'rb'))
        if os.path.exists(prefix + "blocks_by_date.p"):
            pickle.dump(self.blocks_by_date, open(prefix + "blocks_by_date" + ".p", 'rb'))


if __name__ == '__main__':
    # c = pickle.load(open('test_diff_matched.p', 'rb'))
    c = CanonicalStatistics()
    c.start()
    c.save_pickle()
    # c.load_pickle()

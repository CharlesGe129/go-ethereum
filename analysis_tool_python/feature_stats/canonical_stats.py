import statistics
from analysis_tool_python.util.time_format import utc_unix_to_date
from analysis_tool_python.util.cfg import load_cfg
from analysis_tool_python.util.load_file import *


class CanonicalStatistics:
    def __init__(self):
        self.paths = load_cfg()  # [cano, bc, uncle, fork][1=json]
        self.blocks_by_height = dict()  # [height][hash] = block
        self.blocks_by_date = dict()  # [20190910] = list()

        self.mean_daily = dict()  # [field][date] = mean
        self.mean_height = dict()  # [field][height] = mean

        self.total_canonical = 0
        self.total_blocks = 0

        self.miner_stats = dict()  # see func cal_miner_stats()
        self.miner_canonical_num = dict()  # [miner][0=cano, 1=non_cano] = num

        self.differences = dict()  # [field][0=cur-total_mean, 1=cur-mean_height, 2=cur-mean_daily] = list()

        self.overall_stats = dict()  # [field][min, max, std, mean]

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

        # TODO:
        self.organize_difference_1_to_3()

    def load_blocks(self):
        # cano
        self.load_blocks_in_path(self.paths[0][1], True)

        # bc, uncle, fork
        for paths in self.paths[1:]:
            self.load_blocks_in_path(paths[1], False)

    def load_blocks_in_path(self, json_path, is_canonical):
        for filename in load_path(json_path):
            for b in load_json_file_yield_block(json_path, filename):
                height = b.number
                hash_value = b.hash
                if height not in self.blocks_by_height:
                    self.blocks_by_height[height] = dict()
                if hash_value not in self.blocks_by_height[height]:
                    self.blocks_by_height[height][hash_value] = b
                    self.total_blocks += 1
                    if is_canonical:
                        self.total_canonical += 1
                else:
                    self.blocks_by_height[height][hash_value].amend_missing_fields(b)

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

    def cal_mean_and_overall(self, field_and_funcs):
        # field_and_funcs[field=0, get_field_func=1]
        print("calculating mean")
        value_total = dict()  # [field] = list()
        for field_and_func in field_and_funcs:
            field = field_and_func[0]
            value_total[field] = list()
            self.mean_daily[field] = dict()
            self.mean_height[field] = dict()

        print("calculating mean daily")
        # mean daily
        total = len(self.blocks_by_date)
        i = 0
        for date, block_list in self.blocks_by_date.items():
            i += 1
            if i % 10000 == 0:
                print(f"calculate mean daily, process {round(i / total * 100, 3)}%")
            for field_and_func in field_and_funcs:
                field = field_and_func[0]
                get_func = field_and_func[1]
                value_list = [get_func(b) for b in block_list]
                self.mean_daily[field][date] = statistics.mean(value_list)

        print("calculating mean height")
        total = len(self.blocks_by_height)
        i = 0
        # mean height
        for height, blocks_by_hash in self.blocks_by_height.items():
            i += 1
            if i % 10000 == 0:
                print(f"calculate mean height, process {round(i / total * 100, 3)}%")
            for field_and_func in field_and_funcs:
                field = field_and_func[0]
                get_func = field_and_func[1]
                value_list = [get_func(b) for b in blocks_by_hash.values()]
                value_total[field] += value_list
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

    def cal_differences(self, field_and_funcs):
        # field_and_funcs[field=0, get_field_func=1]
        for field_and_func in field_and_funcs:
            field = field_and_func[0]
            get_func = field_and_func[1]
            differences = [list(), list(), list()]
            for date, block_list in self.blocks_by_date.items():
                for b in block_list:
                    differences[0].append(get_func(b) - self.mean_total[field])
                    differences[1].append(get_func(b) - self.mean_height[field][b.number])
                    differences[2].append(get_func(b) - self.mean_daily[field][date])
            self.differences[field] = differences

    def organize_difference_1_to_3(self):
        pass


if __name__ == '__main__':
    c = CanonicalStatistics()
    c.start()
    for k, v in c.overall_stats.items():
        print(k)
        print(v)
    print(123)

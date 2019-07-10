import json
import os
from _datetime import datetime, timezone

'''
EJ Jung [12:13 PM]
1. how many uncles are there, 
2. and how frequently uncle blocks are created, 
3. and also is there any pattern which one becomes canonical 
    and which one becomes uncle, 
    e.g. the one mined by pool x is more likely to become canonical, 
    or the one mined by pool x is more likely to become a parent of another block mined by pool y 
    (and thus becomes canonical) etc
'''
UNCLE_PATH = '../crawler/uncle_sample/'
CANONICAL_PATH = '../crawler/canonical_sample/'


def reverse_dict(data):
    rs = dict()
    for k, v in data.items():
        if v not in rs:
            rs[v] = []
        rs[v].append(k)
    return rs


class Analysis:
    def __init__(self):
        self.uncles = dict()  # dict[hash] = uncle_json_dict
        self.day_freq = dict()  # dict[date] = count_number
        self.hour_freq = dict()  # dict[date+hour] = count_number
        self.minute_freq = dict()  # dict[date+hour+minute] = count_number
        self.overall_hour_freq = dict()
        self.overall_minute_freq = dict()
        self.overall_weekday_freq = dict()

    def start(self):
        self.load_uncles()
        self.count_uncles()

    def load_one_uncle(self, content):
        # one example
        # {"difficulty": "0x757be559a915a",
        # "extraData": "0x65746865726d696e652d7061726974792d6e6f64652d6575",
        #  "gasLimit": "0x7a121d",
        #  "gasUsed": "0x79fae8",
        #  "hash": "0x5624997a439f66fe9548c283ffc312bbbeb0237f9fda22c1f4ab62395e695aea",
        #  "logsBloom": "0xa3cd9866b1569852c07e84024083dd8438d029c143810610c03d0c08648930782034262171c4a94de1809028c869dc5710204c1216102762ea99a48cfde1f00d0d70b8c083144432c979b288d20e1167280d64cd24542110c506bf79bb01680e433409ca7b7937431a386900c2c4de14364411a19900a04f9515169ba4bb2475a4b821ec4099208aaf1749df7a34399639ad9050820d6e22fddf297195f8959a3fc0e02181ea9b81960c03a0c15d16cbc1b686408f07a44203a88b0acdbd6cb25418291b2c4e0282c81864148c4464fb53456f9d282584422258634b096aa69dcd14f2c34528122ccda1b309c84af20865c2f07245d02a2bc9667a6d578e061c",
        #  "miner": "0xea674fdde714fd979de3edf0f56aa9716b898ec8",
        #  "mixHash": "0xbcc8b22765ff402b620d6fc78e42e7f754bddaaaf86ad222492fd01c418bc50b",
        #  "nonce": "0x4cbfa56022370c59",
        #  "number": "0x772bcd",
        #  "parentHash": "0x44dd910602befcb6d6e1bd4c7d1dc727e9fb77ebd750134b1c8b4692d18f636c",
        #  "receiptsRoot": "0x4eefb82608c9130cb3bc9f1077f293c425f5ead6cecc191968cd53dc402ffc39",
        #  "sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
        #  "size": "0x221",
        #  "stateRoot": "0x300ceb70dd73fa66ebc978295c7b7f096ac3cd2a4e3aaef0a3d0775285427ce9",
        #  "timestamp": "0x5ce55405",
        #  "totalDifficulty": "0x22e6573d84f936e19e9",
        #  "transactionsRoot": "0x486cf741ca62002401469dcab1789516b4f04b43aab2b65378940caaaecc9c5e",
        #  "uncles": []}
        data = json.loads(content)
        self.uncles[data['hash']] = data
        t = datetime.fromtimestamp(int(data['timestamp'], 16), timezone.utc)
        day = t.strftime("%Y-%m-%d")
        hour = t.strftime("%Y-%m-%d_%H")
        minute = t.strftime("%Y-%m-%d_%H:%M")
        self.append_freq(self.day_freq, day)
        self.append_freq(self.hour_freq, hour)
        self.append_freq(self.minute_freq, minute)
        self.append_freq(self.overall_hour_freq, t.hour)
        self.append_freq(self.overall_minute_freq, t.minute)
        self.append_freq(self.overall_weekday_freq, t.weekday()+1)

    @staticmethod
    def append_freq(data, k):
        if k not in data:
            data[k] = 0
        data[k] += 1

    def load_uncles(self):
        for filename in os.listdir(UNCLE_PATH):
            if filename.endswith(".txt"):
                print(filename)
                with open(UNCLE_PATH + filename) as f:
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        self.load_one_uncle(line)

    def count_uncles(self):
        print('In sample dataset: \n'
              'From Thursday, May 16, 2019 7:34:19 AM to Friday, June 21, 2019 6:54:41 AM')
        self.statistics(self.day_freq, "===================\nday freq")
        self.statistics(self.hour_freq, "===================\nhour freq")
        self.statistics(self.minute_freq, "===================\nminute freq")
        self.statistics(self.overall_hour_freq, "===================\noverall hour freq")
        self.statistics(self.overall_minute_freq, "===================\noverall minute freq")
        self.statistics(self.overall_weekday_freq, "===================\noverall weekday freq")

    @staticmethod
    def statistics(ori_data, msg):
        print(msg)
        data = reverse_dict(ori_data)
        counts = sorted(data.keys())
        print(f"max_count={counts[-1]}, time={data[counts[-1]]}")
        print(f"min_count={counts[0]}, time={data[counts[0]]}")
        count = 0
        for each in ori_data.values():
            count += each
        print(f"avg_count={count / len(ori_data.keys())}")
        temp = []
        for k, v in ori_data.items():
            temp.append(v)
        nums = sorted(temp)
        if len(nums) % 2 == 1:
            middle = nums[int(len(nums) / 2)]
        else:
            middle = (nums[int(len(nums) / 2)] + nums[int(len(nums) / 2) - 1]) / 2
        print(f"median_count={middle}")

    def test(self):
        # dt = datetime.fromtimestamp(0x5ce34189, timezone.utc)
        # print(dt)
        # print(datetime.fromtimestamp(1558397321, timezone.utc))
        # new_int = int('0x5ce34189', 16)
        # print(hex(new_int))
        # self.get_uncles_frequence()
        # print(self.hex_str_to_datetime('0x5ce34189'))
        # self.load_uncles()
        # print('In sample dataset: \n'
        #       'From Tuesday, May 21, 2019 12:08:41 AM to Friday, June 21, 2019 6:54:41 AM')
        print(len(self.uncles))


if __name__ == '__main__':
    a = Analysis()
    a.start()
    a.test()
    # a.get_uncles_frequence()

import json
import random
import requests
from functools import partial
from multiprocessing import Pool
from datetime import datetime


class UncleCrawler:
    def __init__(self):
        self.base_url = 'https://api.etherscan.io/api?module=proxy&action=eth_getUncleByBlockNumberAndIndex&tag={}&index={}&apikey={}'
        self.api_keys = ['MRIQUZZTIFUAT725VCH6G369Z4MB2GU2P', 'YAZYM9PGKFUAY3XHYM162JB2BV9SB1F7IE',
                         'IX56CFH7GUYEWS1CMK9HBFDEMHJIXKG5S', 'XKKHZVZHRXWKVG6R1SR5Q46T5J2UKFCPAN',
                         'R7WTQ3ZGZ6313ZG5KFZJRCRFYXW7MG37SR', 'VENFADVU89YCV8DYYBT2PRT7WF2WQQVJU4']

    def start(self):
        started_at = datetime.now()
        i = 7800000
        pool = Pool()
        # pool.map(partial(self.loop_10000_pages, thread_num=j), [i])
        while True:
            pool.map(self.loop_10000_pages, [i, i + 10000, i + 20000, i + 30000, i + 40000])
            i -= 50000

    def loop_10000_pages(self, start_num):
        i = 0
        started_at = datetime.now()
        while i < 10000:
            try:
                page_num = start_num + i
                api_key = self.api_keys[random.randint(0, len(self.api_keys) - 1)]
                self.load_uncles(api_key, self.base_url, page_num)
                print(
                    f"Started_num={start_num}: Avg time for {i+1} blocks: {((datetime.now() - started_at).seconds) / (i+1)} seconds\n")
                i += 1
            except Exception as e:
                print(f'Exception {e}. \nRetrying...')

    def load_uncles(self, api_key, base_url, uncle_number):
        uncle_index = 0
        while True:
            url = base_url.format(hex(uncle_number), hex(uncle_index), api_key)
            data = self.load_page(url)
            if not data['result']:
                return
            else:
                self.save(data)
                uncle_index += 1

    @staticmethod
    def load_page(url):
        print(url)
        content = requests.get(url).content
        data = json.loads(content)
        return data

    @staticmethod
    def save(data):
        height = int(data['result']['number'], 16)
        filename = f'./uncle/{int(height / 10000) * 10000}.txt'
        with open(filename, 'a') as f:
            f.write(json.dumps(data['result']))
            f.write('\n')


if __name__ == '__main__':
    UncleCrawler().start()

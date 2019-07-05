import json
import random
import requests
from datetime import datetime


class CanonicalCrawler:
    def __init__(self):
        self.base_url = 'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={}&boolean=false&apikey={}'
        self.api_keys = ['MRIQUZZTIFUAT725VCH6G369Z4MB2GU2P', 'YAZYM9PGKFUAY3XHYM162JB2BV9SB1F7IE', 'IX56CFH7GUYEWS1CMK9HBFDEMHJIXKG5S']

    def start(self):
        started_at = datetime.now()
        for i in range(8000000, 1, -1):
            api_key = self.api_keys[random.randint(0, len(self.api_keys)-1)]
            self.load_page(self.base_url.format(hex(i), api_key))
            # api_key = self.api_keys[random.randint(0, len(self.api_keys)-1)]
            # self.load_page(self.base_url.format(hex(i), api_key))
            # return
            print(f"Average time for {i} blocks: {((datetime.now() - started_at).seconds) / (8000001-i)} seconds")

    def load_page(self, url):
        print(url)
        content = requests.get(url).content
        data = json.loads(content)
        self.save(data)

    def save(self, data):
        height = int(data['result']['number'], 16)
        filename = f'./canonical/{int(height/10000)*10000}.txt'
        with open(filename, 'a') as f:
            f.write(json.dumps(data['result']))
            f.write('\n')


if __name__ == '__main__':
    CanonicalCrawler().start()

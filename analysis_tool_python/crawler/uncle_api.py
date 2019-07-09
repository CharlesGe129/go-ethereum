import json
import random
import requests
from datetime import datetime

class UncleCrawler:
    def __init__(self):
        self.base_url = 'https://api.etherscan.io/api?module=proxy&action=eth_getUncleByBlockNumberAndIndex&tag={}&index={}&apikey={}'
        self.api_keys = ['MRIQUZZTIFUAT725VCH6G369Z4MB2GU2P', 'YAZYM9PGKFUAY3XHYM162JB2BV9SB1F7IE',
                         'IX56CFH7GUYEWS1CMK9HBFDEMHJIXKG5S', 'XKKHZVZHRXWKVG6R1SR5Q46T5J2UKFCPAN',
                         'R7WTQ3ZGZ6313ZG5KFZJRCRFYXW7MG37SR', 'VENFADVU89YCV8DYYBT2PRT7WF2WQQVJU4']

    def start(self):
        started_at = datetime.now()
        i = 7788749
        while True:
            try:
                api_key = self.api_keys[random.randint(0, len(self.api_keys)-1)]
                # data = self.load_page(self.base_url.format(hex(i), api_key))
                self.load_uncles(api_key, self.base_url, i)
                print(f"Average time for {i} blocks: {((datetime.now() - started_at).seconds) / (7788750-i)} seconds\n")
                i -= 1
            except Exception as e:
                print(f'Exception {e}. \nRetrying...')

    def load_uncles(self, api_key, base_url, uncle_number):
        uncle_index = 0
        while True:
            data = self.load_page(base_url.format(hex(uncle_number), hex(uncle_index), api_key))
            if data['result'] == None:
                return
            else:
                self.save(data)
                uncle_index += 1


    def load_page(self, url):
        print(url)
        content = requests.get(url).content
        data = json.loads(content)
        return data
        # self.save(data)

    def save(self, data):
        height = int(data['result']['number'], 16)
        filename = f'./uncle/{int(height/10000)*10000}.txt'
        with open(filename, 'a') as f:
            f.write(json.dumps(data['result']))
            f.write('\n')


if __name__ == '__main__':
    UncleCrawler().start()

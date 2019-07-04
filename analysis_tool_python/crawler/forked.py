import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

soup = BeautifulSoup


class ForkedCrawler:
    def __init__(self):
        self.base_url = 'https://etherscan.io/blocks_forked?ps=100&p='
        self.raw_one_forked = 'https://etherscan.io/block/'
        self.file_path = './forked/'

    def start(self):
        started_at = datetime.now()
        counter = 1
        i = 1
        while i <= 904:
        # for i in range(1, 904):
            url = f"{self.base_url}{i}"
            print(f"loading {url}")
            forked_heights_list = self.load_list_page(url)
            # print(forked_heights_list)
            for forked_height in forked_heights_list:
                info = self.load_detail_page(self.raw_one_forked + forked_height + '/f')
                self.save(info)
                print(f"Average time for {counter} blocks: {((datetime.now()-started_at).seconds) / counter} seconds")
                counter += 1
            i += 1

    @staticmethod
    def load_list_page(url):
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table', {'class': 'table table-hover'})
        rows = table.find('tbody').find_all('tr')
        # 返回的lamdba表达式的详细内容
        # for row in rows:
        #     uncle_td = row.find_all('td')[1]
        #     href = uncle_td.find('a')['href']
        return [row.find_all('td')[0].string for row in rows]

    @staticmethod
    def load_detail_page(url):
        print(f"loading {url}")
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('div', {'class': 'card'}).find('div', {'class': 'card-body'})
        info = {}
        divs = table.find_all('div', {'class': 'col-md-9'})
        info['blockHeight'] = divs[0].find('span').string.strip('\n')
        # print('block height: ', divs[0].find('span').string.strip('\n'))
        # info['timeStampUnformated'] = divs[1].find('i').string.strip('\n')
        # print('time stamp: ', str(divs[1]).split('\n')[-2].split('(')[1].strip(')'))
        info['timeStampUnformated'] = str(divs[1]).split('\n')[-2].split('(')[1].strip(')')
        # print('reorg depth: ', divs[2].string.strip('\n').split('block')[0].strip())
        info['reorgDepth'] = divs[2].string.strip('\n').split('block')[0].strip()
        # print('miner hash: ', divs[3].find('a').string.split(' ')[0])
        info['minerHash'] = divs[3].find('a').string.split(' ')[0]
        # print('miner: ', divs[3].find('a').string.split(' ')[1] if len(divs[6].find('a').string.split(' ')) > 1 else '')
        # print('miner: ', divs[3].find('b').string if divs[3].find('b') else '')
        info['miner'] = divs[3].find('b').string if divs[3].find('b') else ''
        # print('mine time: ', divs[3].text.split('in ')[1].split(' secs')[0])
        info['mineTime'] = divs[3].text.split('in ')[1].split(' secs')[0]
        # print('block reward: ', divs[4].text.split(' Ether')[0].strip('\n'))
        info['reward'] = divs[4].text.split(' Ether')[0].strip('\n')
        # print('uncle reward: ', divs[5].text.strip('\n'))
        info['uncleReward'] = divs[5].text.strip('\n')
        # print('difficulty: ', divs[6].string.strip('\n'))
        info['difficulty'] = divs[6].string.strip('\n')
        # print('total diff: ', divs[7].string.strip('\n'))
        info['totalDifficulty'] = divs[7].string.strip('\n')
        # print('size: ', divs[8].text.strip('\n').split(' bytes')[0])
        info['size'] = divs[8].text.strip('\n').split(' bytes')[0]
        # print('gas used: ', divs[9].text.strip('\n').split(' (')[0])
        info['gasUsed'] = divs[9].text.strip('\n').split(' (')[0]
        # print('gas limit: ', divs[10].string.strip('\n'))
        info['gasLimit'] = divs[10].string.strip('\n')
        # print('extra data: ', divs[11].string.strip('\n'))
        info['extraData'] = divs[11].string.strip('\n')
        # print('hash: ', divs[12].string.strip('\n'))
        info['hash'] = divs[12].string.strip('\n')
        # print('parent hash: ', divs[13].string.strip('\n'))
        info['parentHash'] = divs[13].string.strip('\n')
        # print('sha uncles: ', divs[14].string.strip('\n'))
        info['sha3Uncles'] = divs[14].string.strip('\n')
        # print('nonce: ', divs[15].string.strip('\n'))
        info['nonce'] = divs[15].string.strip('\n')
        return info

    @staticmethod
    def parse_timestamp(info):
        timestamp_list = info['timeStampUnformated'].split(' ')[0].split('-')
        if timestamp_list[0] == 'Jan':
            timestamp_list[0] = '01'
        elif timestamp_list[0] == 'Feb':
            timestamp_list[0] = '02'
        elif timestamp_list[0] == 'Mar':
            timestamp_list[0] = '03'
        elif timestamp_list[0] == 'Apr':
            timestamp_list[0] = '04'
        elif timestamp_list[0] == 'May':
            timestamp_list[0] = '05'
        elif timestamp_list[0] == 'Jun':
            timestamp_list[0] = '06'
        elif timestamp_list[0] == 'Jul':
            timestamp_list[0] = '07'
        elif timestamp_list[0] == 'Aug':
            timestamp_list[0] = '08'
        elif timestamp_list[0] == 'Sep':
            timestamp_list[0] = '09'
        elif timestamp_list[0] == 'Oct':
            timestamp_list[0] = '10'
        elif timestamp_list[0] == 'Nov':
            timestamp_list[0] = '11'
        elif timestamp_list[0] == 'Dec':
            timestamp_list[0] = '12'
        return timestamp_list[0] + '-' + timestamp_list[1] + '-' + timestamp_list[2]

    @staticmethod
    def save(info):
        timestamp = ForkedCrawler.parse_timestamp(info)
        t = time.strptime(timestamp, '%m-%d-%Y')
        filename = time.strftime('%Y-%m-%d', t)
        with open(f'./forked/{filename}.txt', 'a+') as f:
            s = ''
            for k, v in info.items():
                s += f"{k}={v},"
            f.write(s[:-1] + '\n')


if __name__ == '__main__':
    ForkedCrawler().start()

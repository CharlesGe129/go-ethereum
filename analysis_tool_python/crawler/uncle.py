import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

bs = BeautifulSoup


class UncleCrawler:
    def __init__(self):
        self.etherscan_url = 'https://etherscan.io'
        self.list_url_prefix = self.etherscan_url + '/uncles?ps=100&p='
        self.file_path = './uncles/'

    def start(self):
        started_at = datetime.now()
        counter = 1
        for i in range(1, 8963):
            print(f'loading page {i}')
            url = f"{self.list_url_prefix}{i}"
            print(f"loading {url}")
            detail_page_urls = self.load_list_page(url)
            for detail_url in detail_page_urls:
                url = self.etherscan_url + detail_url
                info = self.load_detail_page(url)
                self.save(info)
                print(f"Average time for {counter} blocks: {((datetime.now()-started_at).seconds) / counter} seconds")
                counter += 1

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
        return [row.find_all('td')[1].find('a')['href'] for row in rows]

    @staticmethod
    def load_detail_page(url):
        print(f"loading {url}")
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('div', {'class': 'card'}).find('div', {'class': 'card-body'})
        info = {}
        divs = table.find_all('div', {'class': 'col-md-9'})
        info['uncleHeight'] = divs[0].find('strong').string
        info['unclePosition'] = divs[1].string.strip('\n')
        info['blockHeight'] = divs[2].find('a').string
        info['hash'] = divs[3].string.strip('\n')
        info['parentHash'] = divs[4].string.strip('\n')
        info['sha3Uncles'] = divs[5].string.strip('\n')
        info['minerHash'] = divs[6].find('a').string.split(' ')[0]
        info['miner'] = divs[6].find('a').string.split(' ')[1] if len(divs[6].find('a').string.split(' ')) > 1 else ''
        info['difficulty'] = divs[7].string.strip('\n')
        info['gasLimit'] = divs[8].string.strip('\n')
        info['gasUsed'] = divs[9].string.strip('\n')
        info['timeStampUnformated'] = str(divs[10]).split('\n')[-2].split('(')[1].strip(')')
        info['uncleReward'] = str(divs[11]).split('\n')[-2].replace('<b>', '').replace('</b>', '')
        return info

    @staticmethod
    def save(info):
        t = time.strptime(info['timeStampUnformated'].split(' ')[0], '%m/%d/%Y')
        filename = time.strftime('%Y-%m-%d', t)
        with open(f'./uncles/{filename}.txt', 'a+') as f:
            s = ''
            for k, v in info.items():
                s += f"{k}={v},"
            f.write(s[:-1] + '\n')


if __name__ == '__main__':
    UncleCrawler().start()

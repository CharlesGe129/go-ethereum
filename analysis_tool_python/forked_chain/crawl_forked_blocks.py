import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
Soup = BeautifulSoup

class EthereumForkedBlocks:
    # row written in file:
    # height, data time, Txn, Uncles, miner address, miner name, Gas limit, Difficulty, Reward
    def __init__(self):
        self.raw_url = 'https://etherscan.io/blocks_forked?ps=100&p='

    def start(self):
        for i in range(1, 885):
            print(f'Loading page {i}')
            forked_page = self.load_page(i)
            self.extract_forked_blocks(forked_page)

    def load_page(self, page_number):
        cur_url = self.raw_url + str(page_number)
        return requests.get(cur_url).content

    def extract_forked_blocks(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')
        forked_table = soup.find('table', {'class': 'table table-hover'})
        table_body = forked_table.find('tbody')
        rows = table_body.find_all('tr')
        for r in rows:
            self.extract_one_row(r)

    def extract_one_row(self, row):
        row_content = list()
        # height
        row_content.append(row.find_all('td')[0].string)
        # date time: when the block is found
        row_content.append(row.find_all('td')[1].find('span')['title'])
        # Txn
        row_content.append(row.find_all('td')[2].string)
        # Uncles
        row_content.append(row.find_all('td')[3].string)
        # miner address
        row_content.append(row.find_all('td')[4].find('a')['href'].split('address/')[1])
        # miner name
        row_content.append(row.find_all('td')[4].find('a').string)
        # Gas Limit
        row_content.append(row.find_all('td')[5].string)
        # Difficulty
        row_content.append(row.find_all('td')[6].string)
        # Reward
        if len(row.find_all('td')[7].contents) > 1:
            row_content.append(row.find_all('td')[7].contents[0] + '.' + row.find_all('td')[7].contents[2])
        else:
            row_content.append(row.find_all('td')[7].contents[0])
        # ReorgDepth
        row_content.append(row.find_all('td')[8].string)
        self.save_to_file(row_content)

    def save_to_file(self, row_content):
        with open("../records/forked_blocks_etherscan.txt", 'a') as f:
            f.write(",".join(row_content))
            f.write("\n")

    def load_official(self, official_file_path):
        with open(official_file_path) as f:
            while True:
                line = f.readline()
                if not line:
                    break

if __name__ == '__main__':
    test_efb = EthereumForkedBlocks()
    test_efb.start()
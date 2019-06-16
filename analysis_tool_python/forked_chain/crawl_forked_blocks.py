import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
Soup = BeautifulSoup

class EthereumForkedBlocks:
    def __init__(self):
        self.raw_url = 'https://etherscan.io/blocks_forked?ps=100&p='
        self.table_head = []

    def start(self):
        self.get_table_head(1)
        forked_page = self.load_page(1)
        # get table head from first page
        self.extract_forked_blocks(forked_page)

    def load_page(self, page_number):
        cur_url = self.raw_url + str(page_number)
        return requests.get(cur_url).content

    def get_table_head(self, page_number):
        forked_page = self.load_page(page_number)
        soup = BeautifulSoup(forked_page, 'html.parser')
        table_head = soup.find('thead', {'class': 'thead-light'})
        head_content = table_head.find_all('th')
        for h in head_content:
            self.table_head.append(h.string)

    def extract_forked_blocks(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')
        forked_table = soup.find('table', {'class':'table table-hover'})
        print(forked_table)
        print('===============')
        


    def save_to_file(self):
        pass


if __name__ == '__main__':
    test_efb = EthereumForkedBlocks()
    test_efb.start()

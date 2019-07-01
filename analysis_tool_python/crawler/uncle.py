import requests
from bs4 import BeautifulSoup


soup = BeautifulSoup


class UncleCrawler:
    def __init__(self):
        self.base_url = 'https://etherscan.io/uncles?ps=100&p='
        self.file_path = './uncles/'

    def start(self):
        for i in range(1, 2):
            url = f"{self.base_url}{i}"
            print(f"loading {url}")
            detail_page_urls = self.load_list_page(url)
            for detail_url in detail_page_urls:
                info = self.load_detail_page(detail_url)
                self.save(info)

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
        pass

    @staticmethod
    def save(info):
        pass


if __name__ == '__main__':
    UncleCrawler().start()

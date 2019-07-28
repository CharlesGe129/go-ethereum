import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from urllib.request import Request
import urllib.parse
from functools import wraps

bs = BeautifulSoup


def retry_wrapper(max_retry):
    def decorate(fin):
        @wraps(fin)
        def fout(*args, **kwargs):
            i = 0
            msg = ""
            while i < max_retry:
                try:
                    fin(*args, **kwargs)
                    break
                except Exception as e:
                    print(e)
                    msg += f"[{time.time()}]Err={e}\n"
                    i += 1
            return msg

        return fout

    return decorate


def extract_detail_table(table):
    info = {}
    divs = table.find_all('div', {'class': 'col-md-9'})
    info['blockHeight'] = divs[0].find('span').string.strip('\n')
    info['timeStampUnformated'] = str(divs[1]).split('\n')[-2].split('(')[1].strip(')')
    try:
        info['reorgDepth'] = divs[2].string.strip('\n').split('block')[0].strip()
    except:
        divs = divs[:2] + [''] + divs[2:]
    info['minerHash'] = divs[3].find('a').string.split(' ')[0]
    info['miner'] = divs[3].find('b').string if divs[3].find('b') else ''
    info['mineTime'] = divs[3].text.split('in ')[1].split(' secs')[0]
    info['reward'] = divs[4].text.split(' Ether')[0].strip('\n')
    info['uncleReward'] = divs[5].text.strip('\n')
    info['difficulty'] = divs[6].string.strip('\n')
    info['totalDifficulty'] = divs[7].string.strip('\n')
    info['size'] = divs[8].text.strip('\n').split(' bytes')[0]
    info['gasUsed'] = divs[9].text.strip('\n').split(' (')[0]
    info['gasLimit'] = divs[10].string.strip('\n')
    info['extraData'] = divs[11].string.strip('\n') if divs[11].string else ""
    info['hash'] = divs[12].string.strip('\n')
    info['parentHash'] = divs[13].string.strip('\n')
    info['sha3Uncles'] = divs[14].string.strip('\n')
    info['nonce'] = divs[15].string.strip('\n')
    return info


def log_error(msg):
    with open("forkedErrLog.txt", "a") as f:
        f.write(msg)


class ForkedCrawler:
    def __init__(self):
        self.base_url = 'https://etherscan.io/blocks_forked?ps=100&p='
        self.raw_one_forked = 'https://etherscan.io/block/'
        self.file_path = './forked/'

    def start(self):
        started_at = datetime.now()
        counter = 1
        i = 0
        while i <= 940:
            url = f"{self.base_url}{i}"
            print(f"loading list page {url}")
            forked_heights_list = self.load_list_page(url)
            for forked_height in forked_heights_list:
                if i > 900 and int(forked_height) > 2242199:
                    continue
                elif i < 100 and int(forked_height) <= 8174751:
                    i = 904
                    break
                uri = self.raw_one_forked + forked_height + '/f'
                err_msg = self.load_detail_page(uri)
                if err_msg:
                    log_error(f"uri={uri}\n{err_msg}")
                else:
                    print("Success!")
                print(f"Average time for {counter} blocks: {((datetime.now() - started_at).seconds) / counter} seconds")
                counter += 1
            i += 1

    def retry_error(self):
        started_at = datetime.now()
        counter = 1

        uris = ['https://etherscan.io/block/7814601/f', 'https://etherscan.io/block/7780126/f', 'https://etherscan.io/block/7775512/f', 'https://etherscan.io/block/7750224/f', 'https://etherscan.io/block/7741255/f', 'https://etherscan.io/block/7741021/f', 'https://etherscan.io/block/7740849/f', 'https://etherscan.io/block/7740106/f', 'https://etherscan.io/block/7721891/f', 'https://etherscan.io/block/6404501/f', 'https://etherscan.io/block/6284670/f', 'https://etherscan.io/block/6284665/f', 'https://etherscan.io/block/6284394/f', 'https://etherscan.io/block/6284342/f', 'https://etherscan.io/block/6283568/f', 'https://etherscan.io/block/6283313/f', 'https://etherscan.io/block/6283223/f', 'https://etherscan.io/block/6283124/f', 'https://etherscan.io/block/6283049/f', 'https://etherscan.io/block/6283007/f', 'https://etherscan.io/block/6282959/f', 'https://etherscan.io/block/6212900/f', 'https://etherscan.io/block/6206090/f', 'https://etherscan.io/block/6200097/f', 'https://etherscan.io/block/6181576/f', 'https://etherscan.io/block/6138983/f', 'https://etherscan.io/block/6102703/f', 'https://etherscan.io/block/6052559/f', 'https://etherscan.io/block/5872184/f', 'https://etherscan.io/block/5825178/f', 'https://etherscan.io/block/5804509/f', 'https://etherscan.io/block/5761899/f', 'https://etherscan.io/block/5756106/f', 'https://etherscan.io/block/5746482/f', 'https://etherscan.io/block/5744617/f', 'https://etherscan.io/block/5738175/f', 'https://etherscan.io/block/5734321/f', 'https://etherscan.io/block/5734109/f', 'https://etherscan.io/block/5733099/f', 'https://etherscan.io/block/5716907/f', 'https://etherscan.io/block/5708212/f', 'https://etherscan.io/block/5700837/f', 'https://etherscan.io/block/5697476/f', 'https://etherscan.io/block/5696633/f', 'https://etherscan.io/block/5691421/f', 'https://etherscan.io/block/5676659/f', 'https://etherscan.io/block/5657171/f', 'https://etherscan.io/block/5654873/f', 'https://etherscan.io/block/5171669/f', 'https://etherscan.io/block/5127140/f', 'https://etherscan.io/block/5126930/f', 'https://etherscan.io/block/5126738/f', 'https://etherscan.io/block/5126689/f', 'https://etherscan.io/block/5126672/f', 'https://etherscan.io/block/5016415/f', 'https://etherscan.io/block/4929016/f', 'https://etherscan.io/block/4713624/f', 'https://etherscan.io/block/4681650/f', 'https://etherscan.io/block/4679270/f', 'https://etherscan.io/block/4676378/f', 'https://etherscan.io/block/4676361/f', 'https://etherscan.io/block/4664759/f', 'https://etherscan.io/block/4653709/f', 'https://etherscan.io/block/4640611/f', 'https://etherscan.io/block/4612032/f', 'https://etherscan.io/block/4500785/f', 'https://etherscan.io/block/4435540/f', 'https://etherscan.io/block/4414142/f', 'https://etherscan.io/block/4378156/f', 'https://etherscan.io/block/4369221/f', 'https://etherscan.io/block/4365310/f', 'https://etherscan.io/block/4361298/f', 'https://etherscan.io/block/4337986/f', 'https://etherscan.io/block/4270949/f', 'https://etherscan.io/block/4218107/f', 'https://etherscan.io/block/4210187/f', 'https://etherscan.io/block/4200526/f', 'https://etherscan.io/block/4189811/f', 'https://etherscan.io/block/4186633/f', 'https://etherscan.io/block/4171459/f', 'https://etherscan.io/block/4168745/f', 'https://etherscan.io/block/4156639/f', 'https://etherscan.io/block/4152936/f', 'https://etherscan.io/block/4152566/f', 'https://etherscan.io/block/4123752/f', 'https://etherscan.io/block/4097920/f', 'https://etherscan.io/block/4092666/f', 'https://etherscan.io/block/4071331/f', 'https://etherscan.io/block/4063964/f', 'https://etherscan.io/block/3988826/f', 'https://etherscan.io/block/3967840/f', 'https://etherscan.io/block/3967170/f', 'https://etherscan.io/block/3965847/f', 'https://etherscan.io/block/3926449/f', 'https://etherscan.io/block/3920296/f', 'https://etherscan.io/block/2343133/f', 'https://etherscan.io/block/8214399/f', 'https://etherscan.io/block/8213080/f', 'https://etherscan.io/block/8211212/f', 'https://etherscan.io/block/8210050/f', 'https://etherscan.io/block/8207760/f', 'https://etherscan.io/block/8202686/f', 'https://etherscan.io/block/8200953/f', 'https://etherscan.io/block/8198809/f', 'https://etherscan.io/block/8196831/f', 'https://etherscan.io/block/8194046/f', 'https://etherscan.io/block/8184472/f', 'https://etherscan.io/block/2175148/f', 'https://etherscan.io/block/2173109/f', 'https://etherscan.io/block/2131500/f']
        for uri in uris:
            err_msg = self.load_detail_page(uri)
            if err_msg:
                log_error(f"uri={uri}\n{err_msg}")
            else:
                print("Success!")
            print(f"Average time for {counter} blocks: {((datetime.now() - started_at).seconds) / counter} seconds")
            counter += 1

    @staticmethod
    def load_list_page(url):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        headers = {'user-agent': user_agent}
        while True:
            try:
                content = requests.get(url, headers=headers, timeout=30).content
                soup = BeautifulSoup(content, 'html.parser')
                table = soup.find('table', {'class': 'table table-hover'})
                rows = table.find('tbody').find_all('tr')
                # 返回的lamdba表达式的详细内容
                # for row in rows:
                #     uncle_td = row.find_all('td')[1]
                #     href = uncle_td.find('a')['href']
                return [row.find_all('td')[0].string for row in rows]
            except Exception as e:
                print(f"{e}\nreloading {url}")

    @retry_wrapper(3)
    def load_detail_page(self, url):
        # url = 'http://www.someserver.com/cgi-bin/register.cgi'
        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # values = {'name': 'Michael Foord',
        #           'location': 'Northampton',
        #           'language': 'Python'}
        # headers = {'User-Agent': user_agent}
        #
        # data = urllib.parse.urlencode(values)
        # req = urllib.request.Request(url, data, headers)
        # response = urllib.request.urlopen(req)
        # the_page = response.read()
        # print(the_page)
        print(f"[{datetime.now()}]loading {url}")
        time.sleep(1)
        # f_req = Request(url)
        # f_req.add_header("User-Agent",
        #                  "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36")

        user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"
        headers = {'user-agent': user_agent}

        content = requests.get(url, headers=headers, timeout=30).content
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('div', {'class': 'card'}).find('div', {'class': 'card-body'})
        info = extract_detail_table(table)
        self.save(info)

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

    def test(self):
        test_page_content = self.load_detail_page('https://etherscan.io/block/6222544/f')
        print(test_page_content)


if __name__ == '__main__':
    # ForkedCrawler().start()
    ForkedCrawler().retry_error()
    # test_f = ForkedCrawler()
    # test_f.test()

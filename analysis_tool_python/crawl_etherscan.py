import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
Soup = BeautifulSoup


url_etherscan_pre = 'https://etherscan.io/block/'
url_etherchain_pre = 'https://etherchain.org/block/'


def get_block_page(block_number):
    # /block/block_height or /block/block_hash are both ok
    url = url_etherscan_pre + str(block_number)
    return requests.get(url)


def get_txs_list_page(block_number):
    # use this website because it contains all txs in one page
    url = url_etherchain_pre + str(block_number)
    return requests.get(url).content


def parse_txs_list_page_content(page_content):
    # parse the page and return all txs in list
    tx_list = []

    # print(page_content)
    soup = BeautifulSoup(page_content, 'html.parser')
    txs_table = soup.find('table', attrs={'id':'transactions-table'})
    txs_table_body = txs_table.find('tbody')

    # print(txs_table_body)

    rows = txs_table_body.find_all('tr')
    # read the table row by row
    # each row is a {'Hash':hash_value, 'Type':type, 'From':hash_value, 'To':hash_value, 'Value':xxx ETH, 'Fee':xxx ETH, 'Gas Price':xx GWei, 'Internal Transactions':[{},{}],...}
    # if the a tx does not have internal tx, then 'Internal Transactions':[] is a empty list
    # every row is a {}
    # every row with type Tx is a father row
    # read the next row, if the row is not type Tx, then it is the father row's child, add it to father's 'Internal Transactions' list
    father_tx = {}
    i = 0
    ele_index = 0
    while i < len(rows):
        current_tx = {}
        cols = rows[i].find_all('td')
        # for ele in cols:
        #     print(ele.contents[0])
        # current_tx['Hash'] = cols[0].contents[0]

        # get all href links on this row
        links = rows[i].find_all('a')
        current_tx['Type'] = cols[1].contents[0]
        # current_tx['From'] = cols[2].contents[0].get('href').split('/account/')[1]
        # current_tx['To'] = cols[3].contents[0]
        current_tx['Value'] = cols[4].contents[0]
        current_tx['Fee'] = cols[5].contents[0]
        current_tx['Gas Price'] = cols[6].contents[0]
        current_tx['Internal Transactions'] = []
        if current_tx['Type'] == 'tx':
            current_tx['Hash'] = f"0x{cols[0].contents[0].get('href').split('/tx/')[1]}"
            current_tx['From'] = f"0x{links[1].get('href').split('/account/')[1]}"
            current_tx['To'] = f"0x{links[2].get('href').split('/account/')[1]}"

            tx_list.append(current_tx)
            father_tx = current_tx
        else:
            # the internal tx hash is not recorded
            # could be update later
            try:
                current_tx['Hash'] = ''
                current_tx['From'] = f"0x{links[0].get('href').split('/account/')[1]}"
                current_tx['To'] = f"0x{links[1].get('href').split('/account/')[1]}"
            except:
                print(f"Internal tx parse error with type={current_tx['Type']}")
            if 'Internal Transactions' in father_tx:
                father_tx['Internal Transactions'].append(current_tx)
            else:
                father_tx['Internal Transactions'] = [current_tx]
        i += 1

    tx_list = list(filter(None, tx_list))
    
    # print(tx_list)
    return tx_list

def extract_txs_hash(tx_list):
    pass

def parse_block_page_content(page_content, block_number):
    table_dict = dict()
    soup = BeautifulSoup(page_content, 'html.parser')
    table_content = soup.find(id="ContentPlaceHolder1_maintable")
    info_list = table_content.find_all('div')
    # iteration the table content in html
    i = 0
    while i < len(info_list):
        raw_key = info_list[i]
        i += 1
        raw_value = info_list[i]
        i += 1
        key = raw_key.contents[0].split(':')[0]
        value = raw_value.contents[0]
        table_dict[key] = value

    table_dict['Parent Hash'] = table_dict['Parent Hash'].contents[0]
    table_dict['Mined By'] = table_dict['Mined By'].contents[0]
    table_dict['Height'] = str(block_number)

    # process txs
    # use etherchain instead of etherscan because chain contains all info in one page
    tx_list = parse_txs_list_page_content(get_txs_list_page(block_number))
    table_dict['Transactions'] = tx_list

    table_dict['received status'] = 'inserted'
    return table_dict


def test_parse_block_page_content(page_content, block_number):
    table_dict = dict()
    soup = BeautifulSoup(page_content, 'html.parser')
    table_content = soup.find(id="ContentPlaceHolder1_maintable")
    info_list = table_content.find_all('div', class_='row align-items-center')

    # print('info list type: ', type(info_list))
    # count = 0

    # for div in info_list:
    #     print('count: ', count)
    #     print(div)
    #     count += 1

    # print('\n!!!!!!!!!check!!!!!!!!!!\n')
    # return

    # iteration the table content in html
    i = 0
    while i < len(info_list):
        # print('i: ', i)
        raw_key_value = info_list[i]
        # print('raw key value: ', raw_key_value)

        # print('raw key value contents: ', raw_key_value.contents)
        # print('raw key value contents[1]: ', raw_key_value.contents[1])

        key = raw_key_value.contents[1].text.split(':')[0]
        # print('key: ', key)
        if key == 'Timestamp':
            value = raw_key_value.contents[3].text.split('(')[1].split(')')[0]
        else:
            value = raw_key_value.contents[3].text.split()[0]
        # print('value: ', value, '\n')
        table_dict[key] = value
        i += 1

    # table_dict['Parent Hash'] = table_dict['Parent Hash'].contents[0]
    # table_dict['Mined By'] = table_dict['Mined By'].contents[0]
    table_dict['Height'] = str(block_number)

    # print('table dict: ')
    # for this_key, this_value in table_dict.items():
    #     print(this_key, " : ", this_value)
    # return

    # process txs
    # use etherchain instead of etherscan because chain contains all info in one page
    tx_list = parse_txs_list_page_content(get_txs_list_page(block_number))

    # print('tx list: ', tx_list)

    table_dict['Transactions'] = tx_list

    table_dict['received status'] = 'inserted'

    # print('table dict: ', table_dict)

    # return
    return table_dict


def json_to_string(json_data):
    rs = '[2018] [Inserted]'
    rs += f"Block Hash={json_data['Hash']}, "
    rs += f"number={json_data['Height']}, "
    rs += f"parentHash={json_data['Parent Hash']}, "
    rs += f"uncleHash={json_data['Sha3Uncles']}, "
    # rs += f"timestamp={json_data['TimeStamp'].split('(')[1].split(')')[0]}\n"
    rs += f"timestamp={json_data['Timestamp']}\n"
    for tx in json_data['Transactions']:
        rs += tx['Hash'] + ', '
    rs += '\n'
    return rs


def iteration(block_number, saved_file):
    started_at = datetime.now()
    i = 0
    while True:
        try:
            print('loading block ' + str(block_number))
            page = get_block_page(block_number)
            if 'There are no matching entries' in page.text:
                break
            tx = test_parse_block_page_content(page.content, block_number)
            # print('tx: ', tx)
            # time = tx['TimeStamp'].split('(')[1].split(')')[0]
            time = tx['Timestamp']
            # print('time: ', time)
            # print('tx: ', tx)
            filename = datetime.strptime(time, '%b-%d-%Y %I:%M:%S %p +%Z').replace(tzinfo=None).strftime('%Y-%m-%d')
            with open(saved_file + filename + '.txt', 'a') as f:
                f.write(json_to_string(tx))
            block_number += 1
            i += 1
            print(f"Average time for {i} blocks: {((datetime.now()-started_at).seconds) / i} seconds")
        except Exception as e:
            print(f'Exception {e}. \nRetrying...')


if __name__ == '__main__':
    # iteration(6549581, '../records/blocks/canonical/') AWS
    # iteration(6614825, '../records/blocks/canonical/')  # Ali cloud
    # the earliest received block height is 6355788, so we download the same height in canonical chain
    # since saved canonical blocks stops at 6701076, we start at 6701077
    # aws blocks height: 6355788 - 7121327
    # ali: 6601250 - 7280022
    iteration(7268678, '../records/blocks/canonical/')

import random


class EthereumData:
    def __init__(self):
        # key='hash', value={'created_at': '2018-09-16 08:17:41.392476255 -0700 PDT'}
        self.txs = dict()
        # a block = {'received_status': 'Inserted', 'hash': 'xxx', 'number': '6393659', 'timestamp': '2018-09-24 23:59:22 +0000 UTC', 'txs': ['xxx', 'xxx]}
        self.blocks = list()
        # shard_tx[a][b][1] = {"hash1": tx1, "hash2": tx2}
        self.shard_tx = dict()
        self.num = 0
        self.matched_txs = list()
        self.unmatched_txs = list()

    def load_tx(self, path):
        def parse_new_tx_info(pieces):
            return pieces[0].split("Hash=")[1], {"gas_price": pieces[1].split("GasPrice=")[1],
                                                 "max_fee": pieces[3].split("MaxFee=")[1].strip("\n")}

        def extract_info(line):
            pieces = line.split(", ")
            # New tx has gas info
            (hash_value, tx) = parse_new_tx_info(pieces) if "Hash=" in pieces[0] else (pieces[0].split(" ")[-1].strip("\n"), {})
            tx['created_at'] = pieces[0].split(" m=")[0].strip('[')
            self.txs[hash_value] = tx

        with open(path, 'r') as f:
            while True:
                line = f.readline()
                self.num += 1
                if not line:
                    break
                if line == '\n' or '0x' not in line:
                    continue
                try:
                    extract_info(line)
                except:
                    print(f"Exception at {path}: {line}")
        print(f"Load tx {path} completed. len={len(self.txs)}")
        self.split_txs_into_shards()

    def load_block(self, path):
        def extract_info(block_line, tx_line):
            pieces = block_line.split(", ")
            block = dict()
            block['received_status'] = pieces[0].split('Block Hash')[0].split('[')[-1].split(']')[0]
            block['hash'] = pieces[0].split('Hash=')[1]
            block['number'] = pieces[1].split('number=')[1]
            block['timestamp'] = pieces[2].split('timestamp=')[1].strip('\n')
            block['txs'] = [tx for tx in tx_line.strip(", \n").split(', ') if tx]
            self.blocks.append(block)

        with open(path, 'r') as f:
            while True:
                block_line = f.readline()
                if not block_line:
                    break
                if block_line == '\n':
                    continue
                try:
                    extract_info(block_line, f.readline())
                except:
                    print(f"Exception at {path}: {block_line}")
        print(f"Load block {path} completed. len={len(self.blocks)}")

    def split_txs_into_shards(self):
        print(f"len txs={len(self.txs)}")
        shard_txs = dict()
        i = 0
        dup = 0
        for hash_value, tx in self.txs.items():
            key_1 = hash_value[-1]
            key_2 = hash_value[-2]
            key_3 = hash_value[-3]
            if key_1 not in shard_txs:
                shard_txs[key_1] = dict()
            if key_2 not in shard_txs[key_1]:
                shard_txs[key_1][key_2] = dict()
            if key_3 not in shard_txs[key_1][key_2]:
                shard_txs[key_1][key_2][key_3] = dict()
            if hash_value in shard_txs[key_1][key_2][key_3]:
                dup += 1
                continue
            tx['hash'] = hash_value
            shard_txs[key_1][key_2][key_3][hash_value] = tx
            i += 1
        self.shard_tx = shard_txs
        self.txs.clear()
        print(f"Txs has been split into shards. i={i}, dup={dup}")

    # Match self.shard_txs and self.blocks
    # Pre-work: load tx, load blocks
    def match(self):
        unique_txs = dict()
        for block in self.blocks:
            for tx_hash_value in block['txs']:
                if tx_hash_value in unique_txs:
                    continue
                unique_txs[tx_hash_value] = 1
                self.match_one_tx({'hash': tx_hash_value, 'block_timestamp': block['timestamp']})

    def match_one_tx(self, block_tx):
        key_1 = block_tx['hash'][-1]
        key_2 = block_tx['hash'][-2]
        key_3 = block_tx['hash'][-3]
        if key_1 in self.shard_tx and key_2 in self.shard_tx[key_1] and key_3 in self.shard_tx[key_1][key_2] \
                and block_tx['hash'] in self.shard_tx[key_1][key_2][key_3]:
            tx = self.shard_tx[key_1][key_2][key_3][block_tx['hash']]
            tx['block_timestamp'] = block_tx['block_timestamp']
            self.matched_txs.append(tx)
            self.shard_tx[key_1][key_2][key_3].pop(block_tx['hash'])
        else:
            print(f"Unmatched: {block_tx['hash']}")
            self.unmatched_txs.append(block_tx['hash'])

    # Insert block's txs into txs.txt, with only 20 left
    def prepare_test_file(self):
        self.load_block("test_files/block.txt")
        block_txs = list()
        for each in self.blocks:
            block_txs += each['txs']
        print(len(block_txs))
        self.load_tx("test_files/origin_txs.txt")
        print(len(self.txs))
        length = len(block_txs)
        for i in range(length-20):
            index = random.randint(i*9, i*9+8)
            self.txs[index]['hash'] = block_txs[i]
        print(f"inserted {i}")
        with open('test_files/test_txs.txt', 'w') as f:
            for each in self.txs:
                f.write(f"[{each['created_at']} m=+1.23] {each['hash']}\n")

    def test(self):
        self.load_block("test_files/block.txt")
        self.load_tx("test_files/test_txs.txt")
        self.match()
        assert len(self.txs) == 0, f"len(txs) = {len(self.txs)} is not 0"
        assert len(self.matched_txs) == 513422, f"len(txs) = {len(self.matched_txs)} is not 513422"
        assert len(self.unmatched_txs) == 20, f"len(txs) = {len(self.unmatched_txs)} is not 20"


# data = EthereumData()
# data.load_tx("../records/txs/2018-09-26_15.txt")
# data.load_tx("../records/txs/2018-09-18_03.txt")
# data.load_block("../records/blocks/2018-09-26.txt")
# data.prepare_test_file()
# data.test()

# pickle.dump( favorite_color, open( "save.p", "wb" ) )
# a = pickle.load(open("save.p", "rb"))

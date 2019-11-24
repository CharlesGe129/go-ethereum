import json
from collections import OrderedDict


class Block:
    def __init__(self):
        self.difficulty = ""
        self.extraData = ""
        self.gasLimit = ""
        self.gasUsed = ""
        self.hash = ""
        self.logsBloom = ""
        self.mineTime = ""
        self.miner = ""
        self.minerName = ""
        self.mixHash = ""
        self.nonce = ""
        self.number = 0
        self.parentHash = ""
        self.receiptsRoot = ""
        self.reorgDepth = ""
        self.reward = ""
        self.sha3Uncles = ""
        self.size = ""
        self.stateRoot = ""
        self.timestamp = ""
        self.totalDifficulty = ""
        self.transactions = []
        self.transactionsRoot = ""
        self.txNum = 0
        self.uncleNum = 0
        self.uncleReward = ""
        self.uncles = []

    def to_json(self):
        block_dict = OrderedDict()
        block_dict['difficulty'] = self.difficulty
        block_dict['extraData'] = self.extraData
        block_dict['gasLimit'] = self.gasLimit
        block_dict['gasUsed'] = self.gasUsed
        block_dict['hash'] = self.hash
        block_dict['logsBloom'] = self.logsBloom
        block_dict['mineTime'] = self.mineTime
        block_dict['miner'] = self.miner
        block_dict['minerName'] = self.minerName
        block_dict['mixHash'] = self.mixHash
        block_dict['nonce'] = self.nonce
        block_dict['number'] = self.number
        block_dict['parentHash'] = self.parentHash
        block_dict['receiptsRoot'] = self.receiptsRoot
        block_dict['reorgDepth'] = self.reorgDepth
        block_dict['reward'] = self.reward
        block_dict['sha3Uncles'] = self.sha3Uncles
        block_dict['size'] = self.size
        block_dict['stateRoot'] = self.stateRoot
        block_dict['timestamp'] = self.timestamp
        block_dict['totalDifficulty'] = self.totalDifficulty
        block_dict['transactions'] = self.transactions
        block_dict['transactionsRoot'] = self.transactionsRoot
        block_dict['txNum'] = self.txNum
        block_dict['uncleNum'] = self.uncleNum
        block_dict['uncleReward'] = self.uncleReward
        block_dict['uncles'] = self.uncles
        return json.dumps(block_dict)

    def to_feature_json(self):
        block_dict = OrderedDict()
        block_dict['gasUsed'] = str(self.gasUsed)
        block_dict['gasLimit'] = str(self.gasLimit)
        block_dict['difficulty'] = str(self.difficulty)
        block_dict['number'] = int(self.number)
        block_dict['miner'] = str(self.miner)
        if str(self.timestamp).startswith("0x"):
            block_dict['timestamp'] = str(int(self.timestamp, 16))
        else:
            block_dict['timestamp'] = str(self.timestamp)
        block_dict['size'] = str(self.size)
        block_dict['txNum'] = int(self.txNum)
        block_dict['uncleNum'] = int(self.uncleNum)
        block_dict['hash'] = str(self.hash)
        block_dict['parentHash'] = str(self.parentHash)
        return json.dumps(block_dict)

    def amend_missing_fields(self, b):
        if self.gasUsed == "":
            self.gasUsed = b.gasUsed
        if self.gasLimit == "":
            self.gasLimit = b.gasLimit
        if self.difficulty == "":
            self.difficulty = b.difficulty
        if self.miner == "":
            self.miner = b.miner
        if self.size == "":
            self.size = b.size
        if self.txNum == 0:
            self.txNum = b.txNum
        if self.uncleNum == 0:
            self.uncleNum = b.uncleNum

    def get_value(self, field):
        if field == 'gasUsed':
            return self.gasUsed
        if field == 'gasLimit':
            return self.gasLimit
        if field == 'difficulty':
            return self.difficulty
        if field == 'number':
            return self.number
        if field == 'miner':
            return self.miner
        if field == 'timestamp':
            return self.timestamp
        if field == 'size':
            return self.size
        if field == 'txNum':
            return self.txNum
        if field == 'uncleNum':
            return self.uncleNum
        if field == 'hash':
            return self.hash

import json
from collections import OrderedDict


class Block:
    def __init__(self):
        self.difficulty = ""
        self.extraData = ""
        self.gasLimit = 0
        self.gasUsed = 0
        self.hash = ""
        self.logsBloom = ""
        self.mineTime = ""
        self.miner = ""
        self.minerName = ""
        self.mixHash = ""
        self.nonce = 0
        self.number = 0
        self.parentHash = ""
        self.receiptsRoot = ""
        self.reorgDepth = ""
        self.reward = ""
        self.sha3Uncles = ""
        self.size = 0
        self.stateRoot = ""
        self.timestamp = 0
        self.totalDifficulty = ""
        self.transactions = ""
        self.transactionsRoot = ""
        self.txNum = 0
        self.uncleNum = 0
        self.uncleReward = ""
        self.uncles = ""

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

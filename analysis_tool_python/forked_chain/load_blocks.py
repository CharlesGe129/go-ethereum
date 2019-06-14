import os
from forked_chain import Block


PATH_BLOCK_FOLDER = "../../records/blocks/"
PATH_ALI_BLOCK = PATH_BLOCK_FOLDER + "ali/"
PATH_AWS_BLOCK = PATH_BLOCK_FOLDER + "aws/"
PATH_CANONICAL = PATH_BLOCK_FOLDER + "canonical/"


class Blocks:
    def __init__(self):
        self.blocks_broadcast = dict()  # key=height, value=[]blocks
        self.blocks_canonical = dict()  # key=height, value=one block

    def start(self):
        self.load_blocks_broadcast()
        self.load_blocks_canonical()

# =====================get=======================================
#     def get_block(self, height, blocks):
#         """
#         get broadcast or canonical block based on provided height
#         :parameter
#         height: int
#             wanted blocks' height
#         blocks: dict
#             broadcast or canonical blocks
#
#         :return
#         list of blocks
#         """
#         pass

# =====================broadcast=======================================

    def load_blocks_broadcast(self):
        for folder in [PATH_ALI_BLOCK, PATH_AWS_BLOCK]:
            for filename in os.listdir(folder):
                if filename.endswith(".txt"):
                    self.load_file(f"{folder}{filename}", self.insert)

    def insert(self, block):
        height = block.height
        if height not in self.blocks_broadcast:
            self.blocks_broadcast[int(height)] = list()
        elif self.contains(block):
            return
        self.blocks_broadcast[int(height)].append(block)

    def contains(self, new_block):
        height = int(new_block.height)
        hash_value = new_block.hash_value
        if height not in self.blocks_broadcast:
            return False
        blocks = self.blocks_broadcast[height]
        for block in blocks:
            if block.hash_value == hash_value:
                return True
        return False

    @staticmethod
    def load_file(path, func_insert):
        count = 0
        with open(path) as f:
            while True:
                line = f.readline()
                while line.startswith("0x"):
                    line = f.readline()
                if not line:
                    break
                # line = f.readline()
                line = line.split(']')[-1].strip('\n')
                if path.__contains__('2018-09-20'):
                    # print(line)
                    if line.__contains__('number=6355816'):
                        print('found number=6355816')
                # if line.__contains__('number=6355816'):
                #     print('found 6355816')
                try:
                    hash_value = line.split('Hash=')[1].split(', ')[0]
                    parent_hash = line.split('parentHash=')[1].split(', ')[0]
                    uncle_hash = line.split('uncleHash=')[1].split(', ')[0]
                    height = line.split('number=')[1].split(', ')[0]
                    timestamp = line.split('timestamp=')[1].split(', ')[0]
                    func_insert(Block(int(height), hash_value, None, parent_hash, None))
                    # if int(height) == 6355816:
                    #     print('found: 6355816')
                except Exception as e:
                    print(path)
                    print(e)
                count += 1
        print(f"file={path}, count={count}")

# =====================Canonical=======================================

    def load_blocks_canonical(self):
        for filename in os.listdir(PATH_CANONICAL):
            if filename.endswith('.txt'):
                self.load_file(f"{PATH_CANONICAL}{filename}", self.c_insert)

    def c_insert(self, block):
        height = block.height
        self.blocks_canonical[int(height)] = block

    # 这个应该跟load_file()差不多，我觉得两个函数没啥区别就做成了一个
    def c_load_file(self, path):
        count = 0
        with open(path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if not line.__contains__('Block Hash='):
                    continue
                f.readline()
                line = line.split(']')[-1].strip('\n')
                # print('cur path:')
                # print(path)
                # print('cur line:')
                # print(line)
                hash_value = line.split('Hash=')[1].split(', ')[0]
                parent_hash = line.split('parentHash=')[1].split(', ')[0]
                uncle_hash = line.split('uncleHash=')[1].split(', ')[0]
                height = line.split('number=')[1].split(', ')[0]
                timestamp = line.split('timestamp=')[1].split(', ')[0]
                self.c_insert(Block(int(height), hash_value, None, None))
                count += 1
        print(f"file={path}, count={count}\n")

# ============================================================

    def show(self):
        print('canonical blocks:')
        for key, block in self.blocks_canonical.items():
            print(f'height: {key}')
            print(block.show())

        print('broadcast blocks:')
        for key, block_list in self.blocks_broadcast.items():
            print(f'height: {key}')
            if len(block_list) > 1:
                for b in block_list:
                    print(b.show(), end=' ')

    def canonical_integrity_test(self):
        '''check if canonical blocks are downloaded at all heights'''
        cur_height = 6355788
        last_height = 7415442
        while cur_height <= last_height:
            if cur_height not in self.blocks_canonical:
                print(cur_height)
                break
            cur_height += 1


if __name__ == '__main__':
    test_b = Blocks()
    test_b.start()
    # test_b.show()
    test_b.canonical_integrity_test()
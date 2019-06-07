import os
from analysis_tool_python.forked_chain.forked_chain import Block

PATH_ALI_BLOCK = "../../records/blocks/ali/block/"
PATH_AWS_BLOCK = "../../records/blocks/aws/blocks/"


class Blocks:
    def __init__(self):
        self.blocks_broadcast = dict()  # key=height, value=[]blocks
        self.blocks_canonical = dict()  # key=height, value=one block

    def start(self):
        self.load_blocks_broadcast()
        self.load_blocks_canonical()

    def load_blocks_broadcast(self):
        for folder in [PATH_ALI_BLOCK, PATH_AWS_BLOCK]:
            for filename in os.listdir(folder):
                if filename.endswith(".txt"):
                    self.load_file(f"{folder}{filename}")

    def load_blocks_canonical(self):
        # TODO: 加载canonical blocks
        pass

    def insert(self, block):
        height = block.height
        if height not in self.blocks_broadcast:
            self.blocks_broadcast[height] = list()
        elif self.contains(block):
            return
        self.blocks_broadcast[height].append(block)

    def contains(self, new_block):
        height = new_block.height
        hash_value = new_block.hash_value
        if height not in self.blocks_broadcast:
            return False
        blocks = self.blocks_broadcast[height]
        for block in blocks:
            if block.hash_value == hash_value:
                return True
        return False

    def load_file(self, path):
        count = 0
        with open(path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                f.readline()
                line = line.split(']')[-1].strip('\n')
                hash_value = line.split('Hash=')[1].split(', ')[0]
                parent_hash = line.split('parentHash=')[1].split(', ')[0]
                uncle_hash = line.split('uncleHash=')[1].split(', ')[0]
                height = line.split('number=')[1].split(', ')[0]
                timestamp = line.split('timestamp=')[1].split(', ')[0]
                self.insert(Block(height, hash_value, None, None))
                count += 1
        print(f"file={path}, count={count}")


if __name__ == '__main__':
    Blocks().start()

class Block:
    def __init__(self, height, hash_value, block_type, parent=None, parent_hash=None, peer=None):
        self.height = height
        self.hash_value = hash_value
        self.b_type = block_type
        self.parent = parent
        self.parent_hash = parent_hash
        self.child = list()
        self.peer = peer

    def set_parent(self, parent):
        self.parent = parent
        if parent:
            self.parent_hash = parent.get_hash()
        else:
            self.parent_hash = ""

    def add_child(self, child):
        self.child.append(child)

    def update_peer(self, peer):
        self.peer = peer

    # get parent
    def has_parent(self):
        return self.parent

    # get peer
    def has_peer(self):
        return self.peer

    def get_parent_hash(self):
        if self.parent:
            return self.parent.hash_value
        else:
            return None

    def get_type(self):
        return self.b_type

    def get_hash(self):
        return self.hash_value

    def get_height(self):
        return self.height

    def show(self):
        print(f"self={self.hash_value}, type={self.b_type}, parent={self.get_parent_hash()}", end='')


class ForkedChain:
    def __init__(self):
        # key=height, value=first block
        self.chain = dict()

    def add_block(self, new_block):
        height = new_block.height
        if height not in self.chain:
            self.chain[height] = new_block
        else:
            cur_block = self.chain[height]
            while cur_block.has_peer():
                cur_block = cur_block.peer
            cur_block.update_peer(new_block)

    def get_block(self, height, hash_value):
        if height not in self.chain:
            return None
        cur_block = self.chain[height]
        while cur_block:
            if cur_block.height == height or cur_block.hash_value == hash_value:
                return cur_block
            else:
                cur_block = cur_block.peer
        return None

    def show(self):
        for height in sorted(self.chain.keys()):
            print(f"#{height}, ", end='')
            block = self.chain[height]
            while block:
                block.show()
                print(" => " if block.peer else "", end='')
                block = block.peer
            print()


def test():
    blockA = Block(1, 'A', None)
    blockB = Block(2, 'B', blockA)
    blockC = Block(2, 'C', blockA)
    blockD = Block(3, 'D', blockB)
    blockE = Block(3, 'E', blockC)
    blockF = Block(3, 'F', blockC)
    assert not blockA.has_parent()
    assert blockD.get_parent_hash() == blockB.hash_value
    assert not blockD.has_peer()
    assert not blockE.has_peer()
    assert not blockF.has_peer()
    forked_chain = ForkedChain()
    forked_chain.add_block(blockA)
    forked_chain.add_block(blockB)
    forked_chain.add_block(blockC)
    forked_chain.add_block(blockD)
    forked_chain.add_block(blockE)
    forked_chain.add_block(blockF)
    assert not blockA.has_peer()
    assert blockB.has_peer()
    assert not blockC.has_peer()
    assert blockD.has_peer()
    assert blockE.has_peer()
    assert not blockF.has_peer()
    forked_chain.show()


if __name__ == '__main__':
    test()

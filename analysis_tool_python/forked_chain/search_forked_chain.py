from load_blocks import Blocks
from forked_chain import Block

# TODO: collect each forked chain with detailed blocks


class CheckForkedChain:
    def __init__(self):
        self.blocks = Blocks()

    def start(self, test_mode=False):
        if not test_mode:
            self.blocks.start()
        heights = sorted(self.blocks.blocks_broadcast.keys())
        i_height = 0
        len_heights = len(heights)
        fork_chain_lens = [0]
        while i_height < len_heights:
            cur_height = heights[i_height]
            if cur_height in self.blocks.blocks_canonical:
                # 如果这个高度没有canonical，不做
                canonical_hash = self.blocks.blocks_canonical[cur_height].hash_value
                potential_blocks = self.blocks.blocks_broadcast[cur_height]
                for block in potential_blocks:
                    if block.hash_value == canonical_hash:
                        continue
                    if not self.blocks.contains(block):
                        continue
                    fork_chain_lens.append(self.recur_search_fork(block.height+1, block.hash_value)+1)
            i_height += 1
        print(f"len_of_forked_chains={len(fork_chain_lens)-1}, max_length={max(fork_chain_lens)}, forked_chains={fork_chain_lens}")

    def recur_search_fork(self, height, parent_hash):
        print(f"Recursive_call, height={height}, parent={parent_hash}")
        if height not in self.blocks.blocks_broadcast:
            return 0
        fork_chain_lens = [0]  # 如果没有新的block是从上一个parent_block衍生出来，那就返回0
        potential_blocks = [each for each in self.blocks.blocks_broadcast[height]]  # copy出来，这样之后删除了self.blocks也不会影响到下一个for循环呢
        for block in potential_blocks:
            # 遍历所有当前高度，如果有一个是从parent_block衍生出来的block，就去递归搜索新的forked_tree
            if block.parent_hash == parent_hash:
                print(f"Has a child, hash={block.hash_value}, parent_hash={parent_hash}")
                fork_chain_lens.append(self.recur_search_fork(height+1, block.hash_value)+1)
                self.blocks.blocks_broadcast[height].remove(block)  # 这个block下面整个fork_tree都搜索过，所以删了它，不确定会不会有bug
                print(f"Remove block height={height}, hash={block.hash_value}")
        print(f"return height={height}, parent={parent_hash}, max_fork_len={max(fork_chain_lens)}")
        return max(fork_chain_lens)

    def test(self):
        blockA = Block(1, 'A', None, None)
        blockB = Block(2, 'B', None, None)
        blockC = Block(2, 'C', None, None)
        blockD = Block(3, 'D', None, None)
        blockE = Block(3, 'E', None, None)
        blockF = Block(3, 'F', None, None)
        blockCanonical = Block(1, 'canonical', None, None)
        blockB.parent_hash = 'A'
        blockC.parent_hash = 'A'
        blockD.parent_hash = 'B'
        blockE.parent_hash = 'C'
        blockF.parent_hash = 'C'
        r = CheckForkedChain()
        blocks = Blocks()
        blocks.blocks_broadcast = {
            1: [blockA],
            2: [blockB, blockC],
            3: [blockD, blockE, blockF],
        }
        blocks.blocks_canonical = {
            1: blockCanonical,
            2: blockCanonical,
            3: blockCanonical,
        }
        r.blocks = blocks
        r.start(True)

        blocks.blocks_broadcast = {
            1: [blockA],
            2: [blockB, blockC],
            3: [blockD, blockE, blockF],
        }
        blocks.blocks_canonical = {
            1: blockA,
            2: blockB,
            3: blockD,
        }
        r.blocks = blocks
        r.start(True)

    def test_2(self):
        r = CheckForkedChain()
        blocks = Blocks()
        blocks.start()
        r.blocks = blocks
        r.start(True)


if __name__ == '__main__':
    # CheckForkedChain().test_2()
    r = CheckForkedChain()
    r.start()
    # print(r.blocks.show())
from load_blocks import Blocks
from forked_chain import Block

# TODO: collect each forked chain with detailed blocks


class CheckForkedChain:
    from analysis_tool_python.forked_chain.load_blocks import Blocks
    from analysis_tool_python.forked_chain.forked_chain import Block

    # TODO: Dynamic Program question?

    class CheckForkedChain:
        def __init__(self):
            self.blocks = Blocks()

        def start(self, test_mode=False):
            if not test_mode:
                self.blocks.start()
            heights = sorted(self.blocks.blocks_broadcast.keys())
            i_height = 0
            len_heights = len(heights)
            fork_chains = []
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
                        fork_chains += [[f"{cur_height}:{block.hash_value}"] + child_chain for child_chain in
                                        self.recur_search_fork(block.height + 1, block.hash_value)]
                i_height += 1
            # show
            max_len = 0
            for fork_chain in fork_chains:
                max_len = max(max_len, len(fork_chain))
                print(f"len={len(fork_chain)}, {fork_chain[0]}", end='')
                for each in fork_chain[1:]:
                    print(f" => {each}", end='')
                print()
            print(f"len_of_forked_chains={len(fork_chains)}, max_length={max_len}")

        def recur_search_fork(self, height, parent_hash):
            # print(f"Recursive_call, height={height}, parent={parent_hash}")
            if height not in self.blocks.blocks_broadcast:
                return []
            fork_chains = []  # 如果没有新的block是从上一个parent_block衍生出来，那就返回空
            potential_blocks = [each for each in
                                self.blocks.blocks_broadcast[height]]  # copy出来，这样之后删除了self.blocks也不会影响到下一个for循环呢
            for block in potential_blocks:
                # 遍历所有当前高度，如果有一个是从parent_block衍生出来的block，就去递归搜索新的forked_tree
                if block.parent_hash == parent_hash:
                    # print(f"Has a child, hash={block.hash_value}, parent_hash={parent_hash}")
                    child_chains = self.recur_search_fork(height + 1, block.hash_value)  # e.g.: [[A], [B, C], [B, D]]
                    if len(child_chains) == 0:
                        fork_chains.append([f"{height}:{block.hash_value}"])
                    else:
                        [fork_chains.append([f"{height}:{block.hash_value}"] + child_chain) for child_chain in
                         child_chains]

                    self.blocks.blocks_broadcast[height].remove(block)  # 这个block下面整个fork_tree都搜索过，所以删了它，不确定会不会有bug
                    # print(f"Remove block height={height}, hash={block.hash_value}")
            max_fork_len = 0 if len(fork_chains) == 0 else max([len(each) for each in fork_chains])
            # print(f"return height={height}, parent={parent_hash}, max_fork_len={max_fork_len}")
            return fork_chains

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
            print("====================================")

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

    if __name__ == '__main__':
        # CheckForkedChain().test()
        CheckForkedChain().start()


if __name__ == '__main__':
    # CheckForkedChain().test_2()
    r = CheckForkedChain()
    r.start()
    # print(r.blocks.show())
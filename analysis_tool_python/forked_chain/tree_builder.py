# Tree builder builds the tree (forked chain object)
# Object Blocks loads all blocks and these blocks don't have relationship yet.
# First, build relationship.
#   (always current block's height - 1 = current block parent height)
#   global root locates at height 6355788, where we start to download; its parent block is None
#   while current has child level:
#       one iteration keeps blocks from two continue heights
##
#       iterate every two heights, increasing by 1
#       current_blocks at current height
#       child_blocks at next height
#       update vertical relationship:
#           update current_blocks as child_blocks' parent
#           update child_blocks as current_blocks' children
#       update horizontal relationship:
#           update current blocks at the same height as peers
#       current_blocks = children blocks
#       read next height as children blocks
#
#       repeat iterations until last height, which has no children and child = None

from load_blocks import Blocks
from forked_chain import Block, ForkedChain

class TreeBuilder:
    def __init__(self):
        self.bc_blocks = Blocks()  # broadcast and canonical blocks
        self.forked_chain = ForkedChain()

    def start(self):
        print('loading blocks')
        self.bc_blocks.start()
        print('building relationship')
        self.build_relationship()

    def build_relationship(self):
        cur_height = 6355788  # the global root in canonical
        next_height = cur_height + 1

        # while the children height is not empty, do the iteration
        while next_height in self.bc_blocks.blocks_broadcast:
            # read blocks in two heights
            cur_height_canonical_block = self.bc_blocks.blocks_canonical[cur_height]
            next_height_canonical_block = self.bc_blocks.blocks_canonical[next_height]
            cur_height_broadcast_blocks = self.bc_blocks.blocks_broadcast[cur_height]
            next_height_broadcast_blocks = self.bc_blocks.blocks_broadcast[next_height]
            # update vertical relationship
            # TODO: update
            # update horizontal relationship
            # TODO: update
            # read next height as children blocks
            # TODO: read

if __name__ == '__main__':
    tb = TreeBuilder()
    tb.start()

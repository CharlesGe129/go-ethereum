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


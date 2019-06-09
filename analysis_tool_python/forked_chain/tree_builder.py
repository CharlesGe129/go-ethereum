# Tree builder builds the tree (forked chain object)
# Object Blocks loads all blocks and these blocks don't have relationship yet.
# First, build relationship.
#   (always current block's height - 1 = current block parent height)
#   global root locates at height 6355788, where we start to download
#   while current has child level:
#       one iteration keeps blocks from three continue heights
#
#       blocks have three status: white, grey and black
#       when a block is first touched, which is defined as a child of previous height block, it is white status
#       when a block is iterated as current block, it is grey status
#       when a block is defined as the next block's parent, it is black
#
#       iterate every three heights, increasing by 1
#       update current height block's parent, children, peers
#       black is updated as grey parent,
#       white is update as grey children
#       change status white -> grey -> black
#       read blocks from next height and define as white status
#
#       repeat iterations until last height, which has no children and child = None


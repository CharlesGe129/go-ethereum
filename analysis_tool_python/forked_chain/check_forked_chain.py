# 把所有fork读到内存  根据height和hash去找
# 如果parent是fork，继续往上找；如果parent是canonical，这条forked chain就到头了；如果找不到parent，就报错

#======================================
# first, build the tree
#   load all blocks including canonical ones into the tree
#   canonical is the main branch
#   each block has the type indicating canonical (c), uncle (u), reorged (r), or discard (d).
#   in practise, at first, types are canonical and non canonical,
#   since before analyze data, we don't know if they are uncle, reorged or discard.
#   so, canonical => type c, non canonical => type n
#   EX:
#   #1, self=A, type = c, parent=None
#   #2, self=B, type = c, parent=A => self=C, type = u, parent=A
#   #3, self=D, type = c, parent=B => self=E, type = u, parent=C => self=F, type = d, parent=C
#
# fb_dict[branch_start_height] = forked_branch
# forked branch dictionary stores all forked chains
# key: head height of the forked chain, which is always a canonical block height
# value: customized object forked_chain
#
# second, customized DFS checks branches
#   if canonical node peer number >= 1 or say more than 2 nodes at same height,
#       start DFS search from parent node, which is the local root
#       while this_parent.has_child:
#           current_forked_chain.add(child)
#           this_parent = child
#           (also, peer forked branches belong to this forked chain)
#       when reach leaf (the last block on this branch), add this branch to fb_dict
#       fb_dict[local_root] = current_forked_chain
#
# third, analyze forked branches
#   sort forked branches by tree depth
#       find the longest branch and branches greater than 1
#   sort forked blocks by miner
#       indicate which miners got uncles and un-rewarded blocks
#   etc
#======================================

import os
import sys
from analysis_tool_python.forked_chain.forked_chain import ForkedChain, Block
import collections

AWS_BLOCKS_PATH = '../../records/blocks/aws'
CANONICAL_PATH = '../../records/blocks/canonical'
# https://etherscan.io/block/0xb429b0bad8319d6b0835c57484074d7dc95cb95dd11d00596a2090e9b3271b71/f
# end with 'f' -> forked

all_blocks = {}
# all blocks contains all blocks including canonical blocks
# key: height
# value: dicts of blocks' hash addresses, parent hash and uncle hash at this height
# all_blocks[height] = [block{hash:xxx, parentHash:xxx, uncleHash:xxx}]
canonical_blocks = {}
# canonical_blocks['hash'] = xxx ...
all_forks = []
# [fork1, fork2, ...]
# fork1 = [(height, block), (height, block)]
forks_length = {}
# forks_length[hash] = length
# this dict records the forked block length; it back-counts until reaching canonical chain.
# length 1 means the forked block's parent is a canonical block


class BlockTreeBuilder:
    def __init__(self):
        self.tree = ForkedChain

    def load_blocks(self, folder_path, block_type):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                # print(f"checking {canonical_path}/{file_name}")
                # print('loading file: ', file_name)
                with open(folder_path + '/' + file_name) as f:
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        if line.__contains__('parent'):
                            # print(line)
                            cur_height, cur_hash_value, cur_parent_hash, cur_uncle_hash = self.parse(line)
                            cur_block = Block(cur_height, cur_hash_value, block_type, )
                            canonical_blocks[cur_height] = cur_block

    def parse(self, line):
        '''
        this func parses line content to block object
        :parameter
        line: block information in one line

        :return block object
        '''
        height = line.split('number=')[1].split(',')[0]
        hash_value = line.split('Block Hash=')[1].split(',')[0]
        parent_hash = line.split('parentHash=')[1].split(',')[0]
        uncle_hash = line.split('uncleHash=')[1].split(',')[0]
        return height, hash_value, parent_hash, uncle_hash

    def run(self):
        self.load_blocks(CANONICAL_PATH)
        self.load_blocks(AWS_BLOCKS_PATH)



def load_blocks_in_one_file(blocks_path, file):
    '''block height,
            hash,
            parent hash,
            uncle,
            timestamp
        are loaded
            '''
    # print('loading file: ', file)
    with open(blocks_path+'/'+file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.__contains__('parent'):
                # print(line)
                cur_height, cur_block = load_one_block(line)
                if cur_height not in all_blocks:
                    all_blocks[cur_height] = []
                all_blocks[cur_height].append(cur_block)


def load_canonical(canonical_path):
    for file_name in os.listdir(canonical_path):
        if file_name.endswith('.txt'):
            # print(f"checking {canonical_path}/{file_name}")
            # print('loading file: ', file_name)
            with open(canonical_path + '/' + file_name) as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.__contains__('parent'):
                        # print(line)
                        cur_height, cur_block = load_one_block(line)
                        canonical_blocks[cur_height] = cur_block

def load_one_block(line):
    '''
    line: line contains blocks info, time stamp, hash, parent hash, uncle hash, number and timestamp
    :return block hash, parent hash, uncle hash, height
    '''
    cur_block = {}
    cur_block['hash'] = line.split('Block Hash=')[1].split(',')[0]
    cur_block['parentHash'] = line.split('parentHash=')[1].split(',')[0]
    cur_block['uncleHash'] = line.split('uncleHash=')[1].split(',')[0]
    cur_height = line.split('number=')[1].split(',')[0]
    return cur_height, cur_block


def read_data(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            # print(f"checking {path}/{filename}")
            load_blocks_in_one_file(path, filename)

def chain_forks():
    '''
    Only check blocks smaller than current block
    compare general block with canonical block at the same height, same hash, then pass; different hash, it is a fork
    compare current block's parent hash with previous block hash
    '''
    # first check this block is not canonical
    i = 0
    for height, blocks in all_blocks.items():
        print('process: ', i/len(all_blocks.items()), i, '/', len(all_blocks.items()))
        for block in blocks:
            length = 0
            if is_canonical(height, block):
                continue
            else:
                flag, p_height, p_block = get_parent_block(height, block['parentHash'])
                while flag == 1:
                    length += 1
                    flag, p_height, p_block = get_parent_block(p_height, p_block['parentHash'])
                # if return 0
                # append the canonical block into the list, so we can trace
                if flag == 0:
                    length += 1
                # if return -1
                # error, or parent block is not in the dataset
                # one_fork.append((p_height, p_block))
            if length > 0:
                forks_length[block['hash']] = (height, length)
                print('forked block found at height: ', height, ' ', block)
                print('length: ', length)
        i += 1

def is_canonical(height, block):
    if height in canonical_blocks:
        c_block = canonical_blocks[height]
        if block['hash'] == c_block['hash']:
            return True
        else:
            return False
    else:
        return False


def get_parent_block(cur_height, parent_hash):
    '''
    input parent hash; assuming the forked block parent height may not be current height-1, it could be height-2
    return flag, parent height and parent block
    flag: 0->canonical; 1->fork
    '''
    for c_p_height, c_p_block in canonical_blocks.items():
        # current parent height; current parent block
        if c_p_height < cur_height:
            if c_p_block['hash'] == parent_hash:
                return 0, c_p_height, c_p_block
        else:
            continue

    # check general blocks
    for height, blocks in all_blocks.items():
        if height < cur_height:
            for block in blocks:
                if block['hash'] == parent_hash:
                    return 1, height, block
        else:
            continue

    # if the parent hash is not available in both canonical and general, return -1 meaning error
    return -1, -1, None


if __name__ == '__main__':
    # read_data(AWS_BLOCKS_PATH)
    # print('all block size: ', sys.getsizeof(all_blocks))
    # for height, blocks in all_blocks.items():
    #     if len(blocks) > 1:
    #         temp_set = set()
    #         for b in blocks:
    #             print(b['hash'])
                # temp_set.add(b['hash'])
            # if len(temp_set) >= 5:
            #     print('height: ', height)
            #     print('blocks set: ', temp_set)
            #     print('blocks: ', blocks)
            #     print('len blocks set: ', len(temp_set) , "\n")
    load_canonical(CANONICAL_PATH)
    od = collections.OrderedDict(sorted(canonical_blocks.items()))
    first_height = 6355788
    count = 0
    for height, block in od.items():
        print('height: ', height)
        print('block: ', block)
        print('type height: ', type(height))
        if first_height + count != int(height):
            print('!!!!')
            break
        count += 1
    # print('canonical block size: ', sys.getsizeof(canonical_blocks))

    # filter general dataset, delete canonical blocks from it

    # chain_forks()
    # for hash, b_info in forks_length.items():
    #     print('hash: ', hash)
    #     print('block info: ', b_info)
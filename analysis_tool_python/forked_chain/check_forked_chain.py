# 把所有fork读到内存  根据height和hash去找
# 如果parent是fork，继续往上找；如果parent是canonical，这条forked chain就到头了；如果找不到parent，就报错
import os
import sys

AWS_BLOCKS_PATH = '/Users/Jinyue/Desktop/UC_Davis/EJ_Ethereum/Ethereum_records/aws/blocks'
CANONICAL_PATH = '/Users/Jinyue/Desktop/UC_Davis/EJ_Ethereum/Ethereum_records/Canonical_blocks'
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
    read_data(AWS_BLOCKS_PATH)
    # print('all block size: ', sys.getsizeof(all_blocks))
    for height, blocks in all_blocks.items():
        if len(blocks) > 1:
            temp_set = set()
            for b in blocks:
                # print(b['hash'])
                temp_set.add(b['hash'])
            if len(temp_set) >= 5:
                print('height: ', height)
                print('blocks set: ', temp_set)
                print('blocks: ', blocks)
                print('len blocks set: ', len(temp_set) , "\n")
    # load_canonical(CANONICAL_PATH)
    # for height, block in canonical_blocks.items():
    #     print('height: ', height)
    #     print('block: ', block)
    # print('canonical block size: ', sys.getsizeof(canonical_blocks))

    # filter general dataset, delete canonical blocks from it

    # chain_forks()
    # for hash, b_info in forks_length.items():
    #     print('hash: ', hash)
    #     print('block info: ', b_info)
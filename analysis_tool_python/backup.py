import shutil, os
# from public_functions import get_all_file_name

# this func will move files that are already matched to backup folder

# /go-ethereum/records/blocks
# /go-ethereum/records/txs
# /go-ethereum/records/backup

def backup(file_path, backup_path):
    # caution this func will overwrite old backup
    # call this func only after the matching is finished
    # after processing a txt file, or matching a tx,
    # the file will be move to backup folder
    shutil.move(file_path, backup_path)

# test purpose

# if __name__ == '__main__':
#     file_name_array = get_all_file_name('../../records/txs', '.txt')
#     for name in file_name_array:
#         # dirpath = os.getcwd()
#         # print("current file dir is: " + dirpath)
#         print(name)
#         backup('../../records/txs/{}'.format(name), '../../records/backup/txs/{}'.format(name))
#
#     back_file_name_array = get_all_file_name('../../records/backup/txs', '.txt')
#     for name in back_file_name_array:
#         print(name)

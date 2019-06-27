import os

RECORD_PATH = '../records'

def read_data(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            print(f"checking {path}{filename}")
            load_blocks_in_one_file(path+filename)

def load_blocks_in_one_file(file_path):
    with open(file_path) as f:
        while True:
            line = f.readline()
            if line.__contains__('0x6e10d13cfc0829961d067b62f3898b570b59aca5d008489f1cc9a96b826a69bd'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x6e10d13cfc0829961d067b62f3898b570b59aca5d008489f1cc9a96b826a69bd')
                print('file path: ', file_path)
            if line.__contains__('0x7ce3ec8ff92a6e18cacaa945b65c8259b63d87da9853922026e4fd00684b4aef'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x7ce3ec8ff92a6e18cacaa945b65c8259b63d87da9853922026e4fd00684b4aef')
                print('file path: ', file_path)
            if line.__contains__('0x9e77b4e7bde7db27a1e01e896820a2b73cdaf1c15d965449923688817720ba1c'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x9e77b4e7bde7db27a1e01e896820a2b73cdaf1c15d965449923688817720ba1c')
                print('file path: ', file_path)
            if line.__contains__('0x187568fc430388900ecabbbcc12112b7eddcd61850ea591419417d23e2baae7d'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x187568fc430388900ecabbbcc12112b7eddcd61850ea591419417d23e2baae7d')
                print('file path: ', file_path)
            if line.__contains__('0x073e8f027478683868da2b93fe6065841fdf73c9f2fd24016a74f653565badb4'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x073e8f027478683868da2b93fe6065841fdf73c9f2fd24016a74f653565badb4')
                print('file path: ', file_path)
            if line.__contains__('0x71f68167e64965de1202d9e15f47a635c157bd1c7a5de158854b8548b27814df'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x71f68167e64965de1202d9e15f47a635c157bd1c7a5de158854b8548b27814df')
                print('file path: ', file_path)
            if line.__contains__('0xfb5a174112123bb7ba91be8a9e40fdb356850e119e92fd33e97b44244b0aac91'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0xfb5a174112123bb7ba91be8a9e40fdb356850e119e92fd33e97b44244b0aac91')
                print('file path: ', file_path)
            if line.__contains__('0x4d855818ff4f99ac111fda0eb83e9d7183ff7043a42d773193590eadbf4dac8c'):
                print('!!!!!!!!BLOCK FOUND!!!!!!')
                print('0x4d855818ff4f99ac111fda0eb83e9d7183ff7043a42d773193590eadbf4dac8c')
                print('file path: ', file_path)
            if not line:
                break

if __name__ == '__main__':
    read_data(RECORD_PATH + '/blocks/ali/')
    read_data(RECORD_PATH + '/blocks/aws/')

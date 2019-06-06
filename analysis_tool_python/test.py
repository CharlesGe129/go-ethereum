import os

# with open('/Users/Jinyue/Desktop/uncles.txt') as old_f, open('/Users/Jinyue/Desktop/uncles_new.txt', 'w') as new_f:
#     for line in old_f:
#         if not line.startswith('process:'):
#             new_f.write(line)

def read_data(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            print(filename)

read_data('../records/blocks/aws/')

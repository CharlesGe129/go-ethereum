import os

# with open('/Users/Jinyue/Desktop/uncles.txt') as old_f, open('/Users/Jinyue/Desktop/uncles_new.txt', 'w') as new_f:
#     for line in old_f:
#         if not line.startswith('process:'):
#             new_f.write(line)

# def read_data(path):
#     for filename in os.listdir(path):
#         if filename.endswith(".txt"):
#             print(filename)
#
# read_data('../records/blocks/aws/')

# i = 0
# while i < 20:
#     if i == 15:
#         break
#     if i == 3:
#         continue
#     print(i)
#     i += 1

test_dict = dict()
test_dict[0] = 'z'
test_dict[1] = 'a'
test_dict[2] = 'b'
test_dict[4] = 'd'
i = 0
while i <= 4:
    if i not in test_dict:
        print(i)
        break
    i += 1
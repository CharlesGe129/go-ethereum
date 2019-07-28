import os


class FormatCheck:
    def __init__(self):
        self.path = "./forked/"
        self.wrong_format = dict()  # dict[file_name] = [difficulty, hash, ...]
        self.wrong_format_set = set()

    def start(self):
        for filename in sorted(os.listdir(self.path)):
            if not filename.endswith(".txt"):
                continue
            print(filename)
            with open(f"{self.path}{filename}") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if not line.startswith("blockHeight="):
                        print(line)
                        if filename not in self.wrong_format:
                            self.wrong_format[filename] = list()
                        self.wrong_format[filename].append(line)
                        self.wrong_format_set.add(line.split('=')[0])

            # with open(f"{self.path}{filename}", "w") as f:
            #     f.write(content)
        print(self.wrong_format)
        print(self.wrong_format_set)
        print(len(self.wrong_format_set))

if __name__ == "__main__":
    FormatCheck().start()

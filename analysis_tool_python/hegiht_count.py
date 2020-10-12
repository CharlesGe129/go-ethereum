import json
from analysis_tool_python.util import load_file


class HeightCounter():
    def __init__(self):
        self.wrong_lines = list()
        self.heights = dict()

    def start(self):
        path = '../data/'
        for folder in ['aws_block_tmp/', 'ali/']:
            files = [each for each in load_file.load_path(path + folder)]
            idx = 0
            total = len(files)
            for filename in files:
                idx += 1
                print(f"current progress: {idx / total * 100}%")
                if not filename.endswith('.txt'):
                    continue
                for line in load_file.load_file_yield_lines(path+folder, filename):
                    if line.startswith("tx"):
                        continue
                    self.load_block_line(line)

        self.summary()

    def load_block_line(self, line):
        start_idx = line.index('{')
        if start_idx == 0:
            self.wrong_lines.append(line)
        raw = line[start_idx:].strip()
        try:
            data = json.loads(raw)
        except Exception:
            print("line: ", line)
            print("raw: ", raw)
            print(Exception)


        b_height = data['number']
        b_hash = data['hash']
        if b_height not in self.heights:
            self.heights[b_height] = dict()
        if b_hash not in self.heights[b_height]:
            self.heights[b_height][b_hash] = 1

    def summary(self):
        path = "./height_count.csv"
        print(f"saving height count into {path}")
        keys = sorted(self.heights.keys(), reverse=True)
        with open(path, 'w') as f:
            for key in keys:
                f.write(f"{key},{len(self.heights[key])}\n")

        path = "./error_lines.txt"
        print(f"saving error lines into {path}")
        with open(path, 'w') as f:
            for line in self.wrong_lines:
                f.write(line + "\n")


if __name__ == '__main__':
    HeightCounter().start()

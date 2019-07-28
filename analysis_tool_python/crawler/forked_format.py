import os


class FormatTwoLines:
    def __init__(self):
        self.path = "./forked/"

    def start(self):
        for filename in sorted(os.listdir(self.path)):
            if not filename.endswith(".txt"):
                continue
            filename = f"{self.path}{filename}"
            with open(filename) as f:
                lines = f.readlines()
            content = ""
            for i in range(len(lines)):
                line = lines[i].strip("\n")
                if not line:
                    continue
                elif line.startswith("blockHeight="):
                    if content:
                        content += "\n"
                content += line
            with open(filename, "w") as f:
                f.write(content)


if __name__ == "__main__":
    FormatTwoLines().start()

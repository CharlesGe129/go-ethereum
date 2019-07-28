import os


class FormatTwoLines:
    def __init__(self):
        self.path = "./forked/"

    def start(self):
        for filename in sorted(os.listdir(self.path)):
            if not filename.endswith(".txt"):
                continue
            print(filename)
            with open(f"{self.path}{filename}") as f:
                content = f.read()
            content = content.replace("\n ,parentHash=", " ,parentHash=")
            with open(f"{self.path}{filename}", "w") as f:
                f.write(content)


if __name__ == "__main__":
    FormatTwoLines().start()

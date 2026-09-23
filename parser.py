class Parser:
    def __init__(self, map_file):
        self.parser(map_file)

    def parser(self, map_file: str):

        with open(map_file, "r") as file:
            for line_nb, line in enumerate(file, 1):
                line = line.strip()
                print(line)

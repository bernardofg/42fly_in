# from dataclasses import dataclass
from parser import Parser


class Simulator:
    def __init__(self, map_file: str):
        self.map_file = map_file

    def simulate(self):
        Parser(self.map_file)

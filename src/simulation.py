# from dataclasses import dataclass
from parser import Parser
from map import Graph
from pathfinder import PathFinder


class Simulator:
    def __init__(self, map_file: str):
        self.map_file = map_file

    def simulate(self) -> None:
        parser = Parser(self.map_file)
        graph = Graph(parser.zones, parser.connections, parser.start, parser.end)
        pathfinder = PathFinder(graph)

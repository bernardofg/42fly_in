from models import Zone
from map import Graph
import heapq


class PathFinder:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def heuristic(self, a: Zone, b: Zone) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

# G COST = DISTANCE FROM STARGING NODE
# H COST (HEURISTIC) = DISTANCE FROM END NODE
# F COST = G COST + H COST

    def a_star(self, start: Zone, goal: Zone) -> list[Zone]:
        graph = self.graph
        open_set: list[tuple[float, str]] = [
            (self.heuristic(start, goal), start.name)
            ]
        came_from: dict[str, str] = {}
        g_score: dict[str, float] = {start.name: 0.0}

        while open_set:
            _, _, current = heapq.heappush(open)

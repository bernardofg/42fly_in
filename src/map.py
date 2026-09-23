from models import Zone, Connection


class Graph:
    def __init__(
            self,
            zones: dict[str, Zone],
            connections: list[Connection],
            start: str,
            end: str
            ) -> None:
        self.zones = zones
        self.neighbors: dict[str, list[Zone]] = {}
        self.start = start
        self.end = end

        for name in self.zones:
            self.neighbors[name] = []

        for con in connections:
            a = self.zones[con.zone_a]
            b = self.zones[con.zone_b]
            self.neighbors[a.name].append(b)
            self.neighbors[b.name].append(a)

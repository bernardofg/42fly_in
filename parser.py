from models import Connection, HubKind, Zone, ZoneType

ZONE_KEYS = {"zone", "color", "max_drones"}
CONNECTION_KEYS = {"max_link_capacity"}


class Parser:
    def __init__(self, map_file: str) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.nb_drones: int = 0
        self.start: str | None = None
        self.end: str | None = None
        self.parser(map_file)

    def parser(self, map_file: str) -> None:
        with open(map_file, "r") as file:
            for line_nb, line in enumerate(file, 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    if self.nb_drones != 0:
                        self.error(
                            line_nb, "nb_drones defined more than once")
                    self.nb_drones = self.parse_nb_drones(line, line_nb)

                elif self.nb_drones == 0:
                    self.error(
                        line_nb, "nb_drones must be the first definition")

                elif line.startswith("start_hub:"):
                    if self.start:
                        self.error(
                            line_nb, "start_hub defined more than once")
                    zone = self.parse_zone(line, line_nb, HubKind.START)
                    self.register_zone(zone, line_nb)
                    self.start = zone.name

                elif line.startswith("end_hub:"):
                    if self.end:
                        self.error(line_nb, "end_hub defined more than once")
                    zone = self.parse_zone(line, line_nb, HubKind.END)
                    self.register_zone(zone, line_nb)
                    self.end = zone.name

                elif line.startswith("hub:"):
                    zone = self.parse_zone(line, line_nb, HubKind.HUB)
                    self.register_zone(zone, line_nb)

                elif line.startswith("connection:"):
                    self.parse_connection(line, line_nb)

                else:
                    self.error(line_nb, "Unknown line format")

        if self.nb_drones == 0:
            raise ValueError("Missing nb_drones definition")
        if self.start is None:
            raise ValueError("Missing start_hub definition")
        if self.end is None:
            raise ValueError("Missing end_hub definition")

    def parse_nb_drones(self, line: str, line_nb: int) -> int:
        try:
            value = int(line.split(":")[1].strip())
        except Exception:
            raise ValueError("Invalid nb_drones format")
        if value <= 0:
            self.error(line_nb, "nb_drones must be a positive integer")
        return value

    def parse_zone(self, line: str, line_nb: int, kind: HubKind) -> Zone:
        head, bracket, rest = line.partition("[")
        parts = head.split()
        if len(parts) != 4:
            self.error(line_nb, "Invalid zone format")

        name = parts[1]
        if "-" in name:
            self.error(line_nb, f"Zone name '{name}' must not contain dashes")
        try:
            x = int(parts[2])
            y = int(parts[3])
        except ValueError:
            self.error(line_nb, f"Zone '{name}' has invalid coordinates")

        metadata = self.parse_metadata(bracket + rest, line_nb, ZONE_KEYS)

        raw_type = metadata.get("zone", "normal")
        try:
            zone_type = ZoneType(raw_type)
        except ValueError:
            valid = ", ".join(t.value for t in ZoneType)
            self.error(
                line_nb, f"Invalid zone type '{raw_type}' (valid: {valid})")

        max_drones: int | float
        if kind in (HubKind.START, HubKind.END):
            max_drones = float("inf")
        else:
            max_drones = self.parse_positive_int(
                metadata.get("max_drones", "1"), "max_drones", line_nb)

        return Zone(name, x, y, zone_type, max_drones, metadata.get("color"))

    def register_zone(self, zone: Zone, line_nb: int) -> None:
        if zone.name in self.zones:
            self.error(line_nb, f"Duplicate zone name: '{zone.name}'")
        if any(z.x == zone.x and z.y == zone.y for z in self.zones.values()):
            self.error(
                line_nb, f"Duplicate zone position: ({zone.x}, {zone.y})")
        self.zones[zone.name] = zone

    def parse_connection(self, line: str, line_nb: int) -> None:
        head, bracket, rest = line.partition("[")
        parts = head.split()
        if len(parts) != 2:
            self.error(line_nb, "Invalid connection format")

        names = parts[1].split("-")
        if len(names) != 2 or not all(names):
            self.error(line_nb, f"Invalid connection '{parts[1]}'")
        a, b = names

        if a == b:
            self.error(line_nb, f"Zone '{a}' cannot connect to itself")
        for name in (a, b):
            if name not in self.zones:
                self.error(
                    line_nb, f"Connection references undefined zone '{name}'")

        if any((c.zone_a == a and c.zone_b == b)
               or (c.zone_a == b and c.zone_b == a)
               for c in self.connections):
            self.error(line_nb, f"Duplicate connection: '{a}-{b}'")

        metadata = self.parse_metadata(
            bracket + rest, line_nb, CONNECTION_KEYS)
        raw_cap = metadata.get("max_link_capacity", "1")
        capacity = self.parse_positive_int(
            raw_cap, "max_link_capacity", line_nb)

        self.connections.append(Connection(a, b, capacity))

    def parse_metadata(
        self, raw: str, line_nb: int, allowed: set[str]
    ) -> dict[str, str]:
        raw = raw.strip()
        if not raw:
            return {}
        if not raw.endswith("]"):
            self.error(line_nb, "Metadata must end with ']'")

        content = raw[1:-1]
        if "[" in content or "]" in content:
            self.error(line_nb, "Malformed metadata brackets")

        metadata: dict[str, str] = {}
        for pair in content.split():
            key, sep, value = pair.partition("=")
            if not key or not sep or not value or "=" in value:
                self.error(line_nb, f"Invalid metadata entry '{pair}'")
            if key not in allowed:
                self.error(line_nb, f"Unknown metadata key '{key}'")
            if key in metadata:
                self.error(line_nb, f"Duplicate metadata key '{key}'")
            metadata[key] = value
        return metadata

    def parse_positive_int(self, raw: str, field: str, line_nb: int) -> int:
        try:
            value = int(raw)
        except ValueError:
            self.error(line_nb, f"{field} must be an integer, got '{raw}'")
        if value <= 0:
            self.error(line_nb, f"{field} must be positive, got '{raw}'")
        return value

    def error(self, line_nb: int, msg: str) -> None:
        raise ValueError(f"Line {line_nb}: {msg}")

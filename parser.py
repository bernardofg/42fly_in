from models import Zone, Connection
class Parser:
    def __init__(self, map_file) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.nb_drones: int = 0
        self.start: str | None = None
        self.end: str | None = None
        self.parser(map_file)



    def parser(self, map_file: str):

        with open(map_file, "r") as file:
            for line_nb, line in enumerate(file, 1):
                line = line.strip()

                if line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    pass

                elif line.startswith("start_hub"):
                    pass

                elif line.startswith("end_hub"):
                    pass

                elif line.startswith("hub"):
                    zone = self.parse_zone(line, line_nb)
                    self.zones = zone
                else:
                    pass

    def parse_zone(self,
                   line: str, line_nb: int, parts: list[str], is_start: bool, is_end: bool
                   ) -> Zone:
        parts = line.split()

        name = parts[1]
        if "-" in name or " " in name:
            self.error(line_nb, f"Zone name '{name}' must not contain dashes or spaces")
        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            self.error(line_nb, f"Zone '{name}' has invalid coordinates")
        return (name, x, y)

    def error(self, line_nb: int, msg: str):
        raise ValueError(f"Line {line_nb}: {msg}")
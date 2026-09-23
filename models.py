from dataclasses import dataclass


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    max_drones: int | float = 1
    color: str | None = None
    is_start: bool = False
    is_end: bool = False

@dataclass
class Connection:
    zone_a: str
    zone_b: str
    max_link_capacity: int = 1

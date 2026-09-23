from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubKind(Enum):
    START = "start"
    END = "end"
    HUB = "hub"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int | float = 1
    color: str | None = None


@dataclass
class Connection:
    zone_a: str
    zone_b: str
    max_link_capacity: int = 1

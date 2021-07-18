from enum import IntEnum


class MovementType(IntEnum):
    INGRESS = 1
    EGRESS = 2
    COMMITTED = 3
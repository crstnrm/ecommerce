from enum import IntEnum


class ShipmentStatus(IntEnum):
    CREATED = 1
    SENT = 2
    COMPLETED = 3
    NOT_COMPLETED = 4


class ShipmentProductStatus(IntEnum):
    CREATED = 1
    SENT = 2
    RECEIVED = 3
    RETURNED = 4
    CANCELED = 5

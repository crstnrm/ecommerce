from enum import IntEnum


class OrderStatus(IntEnum):
    CREATED = 1
    PARTIAL_PAYMENT = 2
    PAID = 3
    PARTIAL_SHIPMENT = 4
    SENT = 5
    PROCESSED = 6
    EXPIRED = 7

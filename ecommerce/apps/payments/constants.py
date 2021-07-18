from enum import IntEnum


class PaymentStatus(IntEnum):
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    CANCELED = 4
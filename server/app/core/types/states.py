import enum


class AvailabilityState(enum.StrEnum):
    ACTIVE = "A"
    HIDDEN = "H"
    DISABLED = "D"


class UserState(enum.StrEnum):
    ACTIVE = "A"
    INACTIVE = "I"
    BLOCKED = "B"

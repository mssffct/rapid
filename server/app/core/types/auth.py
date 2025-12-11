import enum


class UserRole(enum.StrEnum):
    DEMO = "D"
    PLAIN_USER = "PU"
    STAFF_ADMIN = "SA"
    LICENSE_ADMIN = "LA"

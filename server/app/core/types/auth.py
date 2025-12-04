import enum


class UserRoles(enum.StrEnum):
    DEMO = "D"
    PLAIN_USER = "PU"
    STAFF_ADMIN = "SA"
    LICENSE_ADMIN = "LA"

import enum

class UserGroupEnum(str, enum.Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"

class GenderEnum(str, enum.Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"

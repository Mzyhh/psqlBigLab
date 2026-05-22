from enum import Enum

class PgType(str):
    def __str__(self):
        raise NotImplementedError

class Varchar(PgType):
    def __init__(self, length=256):
        self.length = length

    def __str__(self):
        return f"VARCHAR({self.length})"

class SimplePgType(PgType, Enum):
    INTEGER = "integer"
    SERIAL = "serial"
    TEXT = "text"
    DATE = "date"
    NUMERIC = "numeric"
    DOUBLE_PRECISION = "double precision"
    BOOLEAN = "boolean"

    def __str__(self):
        return self.value


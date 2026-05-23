from enum import Enum
from datetime import datetime

class PgType:
    def __str__(self):
        raise NotImplementedError

    def format(self, text: str) -> str:
        raise NotImplementedError()

class Varchar(PgType):
    def __init__(self, length=256):
        self.length = length

    def __str__(self):
        return f"VARCHAR({self.length})"

    def format(self, text: str) -> str:
        return text[:self.length]

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

    def format(self, text: str) -> str:
        if text is None:
            return "NULL"

        try:
            if self in (SimplePgType.INTEGER, SimplePgType.SERIAL):
                val = int(text)
                return text

            elif self == SimplePgType.BOOLEAN:
                if text.lower() in ('true', '1', 'yes'):
                    return "TRUE"
                elif text.lower() in ('false', '0', 'no'):
                    return "FALSE"
                else:
                    raise ValueError(f"Invalid boolean value: {text}")

            elif self in (SimplePgType.NUMERIC, SimplePgType.DOUBLE_PRECISION):
                val = float(text)
                return str(val)

            elif self == SimplePgType.DATE:
                s = text.strip()
                dt = None
                
                try:
                    dt = datetime.strptime(s, "%Y-%m-%d")
                except ValueError:
                    pass

                if dt is None:
                    try:
                        dt = datetime.strptime(s, "%d-%m-%Y")
                    except ValueError:
                        raise ValueError(f"Invalid date format '{s}'. Expected YYYY-MM-DD or DD-MM-YYYY.")

                return f"'{dt.strftime('%Y-%m-%d')}'"

            elif self == SimplePgType.TEXT:
                s = text.replace("'", "''")
                return f"'{s}'"

            else:
                return f"'{text}'"

        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert '{text}' to {self.value}: {e}")

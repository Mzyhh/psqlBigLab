from dbtable import *
from pgtypes import *

class Prices(DbTable):
    name = '"Prices"'
    columns = [
        Column("id", SimplePgType.SERIAL, "PRIMARY KEY", ru_name="№"),
        Column("type", SimplePgType.INTEGER, "NOT NULL", ru_name="Тип"),
        Column("cost", SimplePgType.NUMERIC, "CHECK (cost >= 0)", ru_name="Стоимость")

        ]
    
    def primary_key(self):
        return ['id']


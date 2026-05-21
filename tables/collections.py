from dbtable import *
from pgtypes import *

class Collections(DbTable):

    columns = [
        Column("id", SimplePgType.SERIAL, "PRIMARY KEY", "№"),
        Column("name", Varchar(32), "UNIQUE", "Название"),
        Column("description", Varchar(512), ru_name="Описание"),
        Column("start", SimplePgType.DATE, ru_name="Начало"),
        Column('"end"', SimplePgType.DATE, ru_name="Окончание")
    ]
    name = '"Collections"'

    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ['CONSTRAINT end_after_start CHECK ("end" > start)']
    

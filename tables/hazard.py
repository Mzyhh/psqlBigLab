from dbtable import *
from pgtypes import *

class Hazard(DbTable):
    name = '"Hazard"'
    columns = [
        Column("id", SimplePgType.SERIAL, "PRIMARY KEY", ru_name="№"),
        Column("name", Varchar(32), "NOT NULL UNIQUE", ru_name="Название"),
        Column("description", SimplePgType.TEXT)
    ]
    
    def primary_key(self):
        return ['id']

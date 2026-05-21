from dbtable import *
from pgtypes import *

class Halls(DbTable):
    name = '"Halls"'
    columns = [
        Column("id", SimplePgType.SERIAL, "PRIMARY KEY", ru_name="№"),
        Column("name", Varchar(32), "UNIQUE")
    ]
    
    def primary_key(self):
        return ['id']    


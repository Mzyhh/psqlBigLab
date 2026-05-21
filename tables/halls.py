from dbtable import *

class Halls(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Halls"'

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "name": ["varchar(32)", "UNIQUE"]}
    
    def primary_key(self):
        return ['id']    


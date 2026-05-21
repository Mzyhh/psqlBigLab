from dbtable import *

class Hazard(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Hazard"'

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "name": ["varchar(32)", "NOT NULL", "UNIQUE"],
            "description": ["text"]
        }
    
    def primary_key(self):
        return ['id']

from dbtable import *

class Prices(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Prices"'

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "type": ["integer", "NOT NULL"],
            "cost": ["numeric", "CHECK (cost >= 0)"]
        }
    
    def primary_key(self):
        return ['id']


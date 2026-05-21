from dbtable import *

class Items(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Items"'

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "name": ["varchar(64)", "NOT NULL"],
            "description": ["text"],
            "insurance": ["numeric", "CHECK (insurance >= 0)"],
            "century": ["integer"],
            "collection_id": ["integer"],
            "hall_id": ["integer"],
            "height": ["double precision", "CHECK (height >= 0)"],
            "width": ["double precision", "CHECK (width >= 0)"],
            "length": ["double precision", 'CHECK (length >= 0)'],
            "temperature": ["double precision"],
            "wetness": ["double precision", 'CHECK (wetness >= 0)'],
            "safety_level": ["integer"]
        }
    
    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ['CONSTRAINT items_alt_key UNIQUE (name, description)']


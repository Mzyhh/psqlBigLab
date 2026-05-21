from dbtable import *

class Collections(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Collections"'

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "name": ["varchar(32)", "UNIQUE"],
            "description": ["varchar(512)"],
            "start": ["date"],
            "end": ["date"]
        }

    def ru_column_names(self):
        return ["№", "Название", "Описание", "Начало", "Окончание"]
    
    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ['CONSTRAINT end_after_start CHECK ("end" > start)']
    

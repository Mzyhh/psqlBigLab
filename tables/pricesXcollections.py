from dbtable import *

class PricesXCollections(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"PricesXCollections"'

    def columns(self):
        return {
            "price_id": ["integer", "NOT NULL"],
            "collection_id": ["integer", "NOT NULL"]
        }
    
    def primary_key(self):
        return ['price_id', 'collection_id']

#    def column_names_without_id(self):
#        return sorted(self.columns().keys())

#    def table_constraints(self):
#        return [
#            'CONSTRAINT price_fk FOREIGN KEY (price_id) REFERENCES "Prices" (id)',
#            'CONSTRAINT collection_fk FOREIGN KEY (collection_id) REFERENCES "Collections" (id)'
#        ]

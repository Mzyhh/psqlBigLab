from dbtable import *
from pgtypes import *

class PricesXCollections(DbTable):
    name = '"PricesXCollections"'
    columns = [
        Column("price_id", SimplePgType.INTEGER, "NOT NULL", ru_name="№ билета"),
        Column("collection_id", SimplePgType.INTEGER, "NOT NULL", ru_name="№ коллекции")
            ]
    
    def primary_key(self):
        return ['price_id', 'collection_id']

#    def column_names_without_id(self):
#        return sorted(self.columns().keys())

#    def table_constraints(self):
#        return [
#            'CONSTRAINT price_fk FOREIGN KEY (price_id) REFERENCES "Prices" (id)',
#            'CONSTRAINT collection_fk FOREIGN KEY (collection_id) REFERENCES "Collections" (id)'
#        ]

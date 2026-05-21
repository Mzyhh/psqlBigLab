from dbtable import *

class Items(DbTable):
    name = '"Items"'
    columns = [
        Column("id", SimplePgType.SERIAL, "PRIMARY KEY", ru_name="№"),
        Column("name", Varchar(64), "NOT NULL", ru_name="Название"),
        Column("description", SimplePgType.TEXT, ru_name="Описание"),
        Column("insurance", SimplePgType.NUMERIC, "CHECK (insurance >= 0)", ru_name="Страховая стоимость"),
        Column("century", SimplePgType.INTEGER, ru_name="Век"),
        Column("collection_id", SimplePgType.INTEGER, ru_name="№ коллекции"),
        Column("hall_id", SimplePgType.INTEGER, ru_name="№ зала"),
        Column("height", SimplePgType.DOUBLE_PRECISION, "CHECK (height >= 0)", ru_name="Высота"),
        Column("width", SimplePgType.DOUBLE_PRECISION, "CHECK (width >= 0)", ru_name="Ширина"),
        Column("length", SimplePgType.DOUBLE_PRECISION, "CHECK (length >= 0)", ru_name="Длина"),
        Column("temperature", SimplePgType.DOUBLE_PRECISION, ru_name="Температура"),
        Column("wetness", SimplePgType.DOUBLE_PRECISION, "CHECK (wetness >= 0)", ru_name="Влажность"),
        Column("safety_level", SimplePgType.INTEGER, ru_name="Уровень охранения")
    ]

    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ['CONSTRAINT items_alt_key UNIQUE (name, description)']

    def all_by_coll_id(self, coll_id: int):
        sql = f"SELECT * FROM {self.table_name()} WHERE collection_id = {coll_id};" 
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        while True:
            record = cur.fetchone()
            if record is None:
                break
            yield record


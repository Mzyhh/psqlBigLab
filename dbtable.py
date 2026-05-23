from dataclasses import dataclass
from dbconnection import *
from pgtypes import *

@dataclass
class Column:
    name: str
    ru_name: str | None
    pgtype: PgType
    constraints: str

    def __init__(self, name, pgtype, constraints="", ru_name=None):
        self.name = name
        self.pgtype = pgtype
        self.constraints = constraints
        self.ru_name = ru_name

    def __str__(self) -> str:
        return " ".join([self.name, str(self.pgtype), self.constraints])

class DbTable:
    name: str = "table"
    dbconn: DbConnection = None
    columns: list[Column] = [Column('test', SimplePgType.INTEGER, 'primary key', ru_name='Тест')]
    _columns_dict: dict[str, Column] = {}

    @property
    def columns_dict(self) -> dict[str, Column]:
        if len(self._columns_dict) == 0:
            for col in self.columns:
                self._columns_dict[col.name] = col
        return self._columns_dict 

    def table_name(self):
        if self.dbconn is None:
            raise ValueError("DbConnection should be setted!")
        return self.dbconn.prefix + self.name

    def column_names(self) -> list[str]:
        return [col.name for col in self.columns]

    def ru_column_names(self):
        return [col.ru_name for col in self.columns]

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        res = self.column_names()
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE IF NOT EXISTS "+ self.table_name() + "("
        arr = [str(col) for col in self.columns]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()

    def truncate(self, restart_id=False, cascade=False):
        sql = f"TRUNCATE {self.table_name()} {'RESTART IDENTITY' if restart_id else ''} {'CASCADE' if cascade else ''};"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()

    def delete_by_id(self, id):
        try:
            sql = f"DELETE FROM {self.table_name()} WHERE id = {id};"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql)
            self.dbconn.conn.commit()
        except Exception as e:
            self.dbconn.conn.rollback()
            raise e 

    def find_by_id(self, id):
        try:
            sql = f"SELECT * FROM {self.table_name()} WHERE id = {id};"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()
        except Exception as e:
            raise e 

    def insert_one(self, vals):
        cols = ", ".join(self.column_names_without_id())
        placeholders = ", ".join(["%s"] * len(vals))
        sql = f"INSERT INTO {self.table_name()} ({cols}) VALUES ({placeholders})"
        
        cur = self.dbconn.conn.cursor()

        try:
            cur.execute(sql, vals) # драйвер сам всё делает
            self.dbconn.conn.commit()
        except Exception as e:
            self.dbconn.conn.rollback()
            print('Не удалось добавить: неправильный формат ввода')
            return
        

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()        

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        while True:
            row = cur.fetchone() # NOTE: think about fetchmany
            if row is None:
                break
            yield row
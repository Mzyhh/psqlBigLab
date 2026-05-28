# import sys
# sys.path.append('tables')
from rich.console import Console
from rich.table import Table
from itertools import cycle

from project_config import *
from dbconnection import *
from dbtable import *
from tables import *

COLORS = ["magenta", "green", "yellow", "red", "blue"]

DEBUG = True

MAIN_MENU = "0"
WATCH_COLL = "1"
RESTART_DB = "2"
NEW_COLL = "3"
DEL_COLL = "4"
WATCH_ITEMS = "5"
EDIT_COLL = "6"
NEW_ITEM = "7"
DEL_ITEM = "8"
EXIT = "9"

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)
    console = Console()

    def __init__(self):
        DbTable.dbconn = self.connection
        self.tables: dict[str, DbTable] = {
            'Collections': Collections(),
            'Items': Items(),
        }

    def db_init(self):
        for table in self.tables.values():
            table.create()

    def db_insert_somethings(self):
        cur = self.connection.conn.cursor()
        with open('queries/example_fill_tables.sql') as f:
            sql = "".join(f.readlines())
            cur.execute(sql)
        self.connection.conn.commit()

    def db_drop(self):
        for table in self.tables.values():
            table.truncate(restart_id=True, cascade=True)

    def read_next_step(self):
        return input("=> ").strip()


    # Collection stuff

    def show_collections(self):
        table = Table(title="Коллекции")
        for col, style in zip(self.tables["Collections"].columns, cycle(COLORS)):
            table.add_column(col.ru_name, style=style)

        for record in self.tables["Collections"].all():
            table.add_row(*[str(x) for x in record])
        self.console.print(table)

        menu = f"""Дальнейшие операции: 
    {MAIN_MENU} - возврат в главное меню;
    {NEW_COLL} - добавление новой коллекции;
    {DEL_COLL} - удаление коллекции;
    {WATCH_ITEMS} - просмотр экспонатов в коллекции;
    {EDIT_COLL} - редактирование коллекции
    {EXIT} - выход."""
        print(menu)

    def remove_collection(self):
        while True:
            try:
                n = int(input("Введите порядковый номер коллекции (-1 - для отмены): "))
                if n == -1:
                    return WATCH_COLL
            except Exception as e:
                print("Ну совсем плохой ввод, попробуйте еще раз!") 

            try:
                self.tables["Collections"].delete_by_id(n)
                break
            except Exception as e:
                print('Несуществующий идентификатор')

        return WATCH_COLL
    
    def edit_collection(self):
        data = []
        id = input("Введите № коллекции, которую хотите изменить: ")

        for col_name in self.tables["Collections"].column_names_without_id():
            col = self.tables["Collections"].columns_dict[col_name]
            while True:
                
                value = input(f"Введите значение поля {col.ru_name} (-1 - отмена): ").strip()
                if value == "-1":
                    return
                try:
                    break
                except Exception as e:
                    print("Попробуйте еще раз.")
            data.append(value)
        self.tables["Collections"].edit_by_id(id, data)

    def show_add_collection(self):
        data = []
        for col_name in self.tables["Collections"].column_names_without_id():
            col = self.tables["Collections"].columns_dict[col_name]
            while True:
                value = input(f"Введите значение поля {col.ru_name} (-1 - отмена): ").strip()
                if value == "-1":
                    return
                try:
                    value = col.pgtype.format(value)
                    break
                except Exception as e:
                    print(str(e))
                    print("Попробуйте еще раз.")
            data.append(value)
        self.tables["Collections"].insert_one(data)

    def get_collection(self):
        """Ask user for collection id and returns object (or None if user canceled input)"""
        obj = None
        while True:
            num = input("Укажите номер коллекции, в которой вы хотите посмотреть экспонаты (-1 - отмена): ")
            while len(num.strip()) == 0:
                num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас коллекция (-1 - отмена):").strip()
            if num == "-1":
                return None, -1
            try:
                obj = self.tables["Collections"].find_by_id(num)
                if obj is None:
                    raise ValueError("Bad id")
                break
            except Exception as e:
                if DEBUG:
                    print("DEBUG MESSAGE: " + str(e))
                print("Неверный порядковый номер!")
        return obj

    def show_items_by_collection(self, collection):
        table = Table(title=f"Экспонаты коллекции {collection[1]}")
        for col, style in zip(self.tables["Items"].columns, cycle(COLORS)):
            table.add_column(col.ru_name, style=style)

        for record in self.tables["Items"].all_by_coll_id(str(collection[0])):
            table.add_row(*[str(x) for x in record])
        self.console.print(table)

    def add_new_item(self, coll_id):
        skip_fields = set(["hall_id", "safety_level"]) 
        data = []
        for col_name in self.tables["Items"].column_names_without_id():
            col = self.tables["Items"].columns_dict[col_name]
            if col.name in skip_fields:
                data.append(WATCH_COLL)
                continue
            if col.name == "collection_id":
                data.append(str(coll_id))
                continue
            while True:
                value = input(f"Введите значение поля {col.ru_name} (1 - отмена): ").strip()
                if value == WATCH_COLL:
                    return
                try:
                    value = col.pgtype.format(value)
                    break
                except Exception as e:
                    print("Попробуйте еще раз.")
            data.append(value)
        self.tables["Items"].insert_one(data)

    def remove_item(self):
        while True:
            try:
                n = int(input("Введите номер экспоната (-1 - для отмены): "))
                if n == -1:
                    break
            except Exception as e:
                print("Ну совсем плохой ввод, попробуйте еще раз!") 
                continue

            try:
                self.tables["Items"].delete_by_id(n)
                break
            except Exception as e:
                if DEBUG:
                    print("DEBUG: ", str(e))
                print('Несуществующий номер')

    def show_main_menu(self):
        menu = f"""Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    {WATCH_COLL} - просмотр коллекций
    {RESTART_DB} - сброс и инициализация таблиц;
    {EXIT} - выход."""
        print(menu)
        return

    def after_show_collections(self, next_step):
        while True:
            if next_step == DEL_COLL:
                self.remove_collection()
                return WATCH_COLL
            elif next_step == NEW_COLL:
                self.show_add_collection()
                next_step = WATCH_COLL
            elif next_step == WATCH_ITEMS:
                collection = self.get_collection()
                if collection is None:
                    next_step = WATCH_COLL
                else:
                    next_step = self.items_menu(collection)
            elif next_step == EDIT_COLL:
                self.edit_collection()
                return WATCH_COLL
            elif next_step != MAIN_MENU and next_step != EXIT and next_step != WATCH_COLL:
                print("Выбрано неверное число! Повторите ввод!")
                return WATCH_COLL
            else:
                return next_step

    def items_menu(self, collection):
        menu = f"""Действия с экспонатами:
    {WATCH_COLL} - перейти в меню коллекций
    {NEW_ITEM} - добавление новых экспонатов в коллекцию;
    {DEL_ITEM} - удаление экспонатов из коллекции
    {EXIT} - выход."""
        while True:
            self.show_items_by_collection(collection)
            print(menu)
            next_step = self.read_next_step()

            if next_step == NEW_ITEM:
                self.add_new_item(str(collection[0]))
            elif next_step == DEL_ITEM:
                self.remove_item()
            elif next_step in "19":
                return next_step
            else:
                print("Выбрано неверное число! Повторите ввод!")

    def after_main_menu(self, next_step):
        if next_step == RESTART_DB:
            self.db_drop()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return MAIN_MENU
        elif next_step not in [WATCH_COLL, NEW_COLL, EXIT]:
            print("Выбрано неверное число! Повторите ввод!")
            return MAIN_MENU
        else:
            return next_step
            
    def main_cycle(self):
        self.db_init()
        current_menu = MAIN_MENU
        next_step = None
        while(current_menu != EXIT):
            if current_menu == MAIN_MENU:
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == WATCH_COLL:
                self.show_collections()
                next_step = self.read_next_step()
                current_menu = self.after_show_collections(next_step)
            elif current_menu == RESTART_DB:
                self.show_main_menu()
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# m.test()
m.main_cycle()
    

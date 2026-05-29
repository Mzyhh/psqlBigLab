from rich.console import Console
from rich.table import Table
from itertools import cycle
from datetime import date

from project_config import *
from dbconnection import *
from dbtable import *
from tables import *

COLORS = ["magenta", "green", "yellow", "red", "blue"]

DEBUG = False

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
        
        # Скрываем колонку ID из заголовков
        for col, style in zip(self.tables["Collections"].columns, cycle(COLORS)):
            if col.name == 'id':
                continue
            table.add_column(col.ru_name, style=style)

        # Скрываем ID из строк при выводе
        for record in self.tables["Collections"].all():
            row_vals = []
            for col, val in zip(self.tables["Collections"].columns, record):
                if col.name != 'id':
                    row_vals.append(str(val))
            table.add_row(*row_vals)
            
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
            name = input("Введите НАЗВАНИЕ коллекции для удаления (-1 - для отмены): ").strip()
            if name == "-1":
                return WATCH_COLL
            if len(name) == 0:
                print("Пустая строка. Повторите ввод!")
                continue

            try:
                # Удаляем по названию
                self.tables["Collections"].delete_by_name(name)
                break
            except Exception as e:
                if DEBUG:
                    print("DEBUG: ", str(e))
                print('Несуществующее название коллекции. Попробуйте еще раз.')

        return WATCH_COLL
    
    def edit_collection(self):
        collection = self.get_collection()
        if collection is None:
            return

        data = []
        # Проходим по всем колонкам, кроме id, сохраняя правильный индекс для подстановки старых значений
        for col in self.tables["Collections"].columns:
            if col.name == 'id':
                continue
            
            idx = self.tables["Collections"].columns.index(col)
            while True:
                value = input(f"Введите значение поля {col.ru_name} (-1 - отмена, пустая строка - оставить как есть): ").strip()
                if value == "-1":
                    return
                if len(value) == 0:
                    value = str(collection[idx])
                    break

                try:
                    value = col.pgtype.format(value)
                    break
                except Exception as e:
                    print("Неверный формат. Попробуйте еще раз.")
            data.append(value)
        if DEBUG:
            print("DEBUG: ", data)
        self.tables["Collections"].edit_by_id(collection[0], data)

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
                    if col_name == '"end"' and date.fromisoformat(data[-1][1:-1]) > date.fromisoformat(value[1:-1]):
                        print("Конец не может быть раньше начала. Попробуйте еще раз.")
                        continue
                    break
                except Exception as e:
                    if DEBUG:
                        print("DEBUG: ", str(e))
                    print("Попробуйте еще раз.")
            data.append(value)
        self.tables["Collections"].insert_one(data)

    def get_collection(self):
        """Ask user for collection name and returns object row (or None if user canceled input)"""
        obj = None
        while True:
            name = input("Укажите НАЗВАНИЕ интересующей Вас коллекции (-1 - отмена): ").strip()
            if name == "-1":
                return None
            if len(name) == 0:
                print("Пустая строка. Повторите ввод!")
                continue
            try:
                # Ищем запись в БД по названию
                obj = self.tables["Collections"].find_by_name(name)
                if obj is None:
                    raise ValueError("Bad name")
                break
            except Exception as e:
                if DEBUG:
                    print("DEBUG MESSAGE: " + str(e))
                print("Неверное название коллекции!")
        return obj

    def show_items_by_collection(self, collection):
        table = Table(title=f"Экспонаты коллекции {collection[1]}")
        
        # Скрываем колонку ID из заголовков экспонатов
        for col, style in zip(self.tables["Items"].columns, cycle(COLORS)):
            if col.name == 'id':
                continue
            table.add_column(col.ru_name, style=style)

        # Скрываем ID из строк экспонатов
        for record in self.tables["Items"].all_by_coll_id(str(collection[0])):
            row_vals = []
            for col, val in zip(self.tables["Items"].columns, record):
                if col.name != 'id':
                    row_vals.append(str(val))
            table.add_row(*row_vals)
            
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
            name = input("Введите НАЗВАНИЕ экспоната для удаления (-1 - для отмены): ").strip()
            if name == "-1":
                break
            if len(name) == 0:
                print("Пустая строка. Повторите ввод!")
                continue

            try:
                # Удаляем по названию (предполагается, что колонка называется 'name')
                self.tables["Items"].delete_by_name(name)
                break
            except Exception as e:
                if DEBUG:
                    print("DEBUG: ", str(e))
                print('Несуществующее название экспоната')

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
m.main_cycle()
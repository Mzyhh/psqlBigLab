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

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр коллекций;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_collections(self):
        table = Table(title="Коллекции")
        for col, style in zip(self.tables["Collections"].columns, cycle(COLORS)):
            table.add_column(col.ru_name, style=style)

        for record in self.tables["Collections"].all():
            table.add_row(*[str(x) for x in record])
        self.console.print(table)

        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление новой коллекции;
    4 - удаление коллекции;
    5 - просмотр экспонатов в коллекции;
    6 - редактирование коллекции
    9 - выход."""
        print(menu)

    def remove_collection(self):
        while True:
            try:
                n = int(input("Введите порядковый номер коллекции (-1 - для отмены): "))
                if n == -1:
                    return "1"
            except Exception as e:
                print("Ну совсем плохой ввод, попробуйте еще раз!") 

            try:
                self.tables["Collections"].delete_by_id(n)
                break
            except Exception as e:
                print('Несуществующий идентификатор')

        return "1"
    
    def edit_collection(self):
        data = []
        id = input("Введите id коллекции, которую хотите изменить")

        for col_name in self.tables["Collections"].column_names_without_id():
            col = self.tables["Collections"].columns_dict[col_name]
            while True:
                
                value = input(f"Введите значение поля {col.ru_name} (1 - отмена)").strip()
                if value == "1":
                    return
                try:
                    break
                except Exception as e:
                    print("Попробуйте еще раз.")
            data.append(value)
        self.tables["Collections"].edit_by_id(id, data)


    def after_show_collections(self, next_step):
        while True:
            if next_step == "4":
                self.remove_collection()
                return "1"
            elif next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_items_by_collection()
            elif next_step == "6":
                self.edit_collection()
                return "1"
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_collection(self):
        data = []
        for col_name in self.tables["Collections"].column_names_without_id():
            col = self.tables["Collections"].columns_dict[col_name]
            while True:
                value = input(f"Введите значение поля {col.ru_name} (1 - отмена)").strip()
                if value == "1":
                    return
                try:
                    break
                except Exception as e:
                    print("Попробуйте еще раз.")
            data.append(value)
        self.tables["Collections"].insert_one(data)

#        max_len = self.tables["Collections"].columns_dict["name"].pgtype.length
#        name = input("Введите название (1 - отмена): ").strip()
#        if name == "1":
#            return
#        while (isempty := len(name) == 0) or len(name) > max_len:
#            if isempty:
#                name = input("Имя не может быть пустым! Введите имя заново (1 - отмена):").strip()
#            else:
#                name = input(f"Слишком длинное имя (максимум {max_len} символа) (1 - отмена):").strip()
#            if name == "1":
#                return
#        data.append(name)
#
#        max_len = self.tables["Collections"].columns_dict["description"].pgtype.length
#        description = input("Введите описание (1 - отмена): ").strip()
#        if description == "1":
#            return
#        while (isempty := len(description) == 0) or len(description) > max_len:
#            if isempty:
#                description = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
#            else:
#                description = input(f"Слишком длинное описание (максимум {max_len} символов (1 - отмена)):").strip()
#            if description == "1":
#                return
#        data.append(description)
#
#        start_time = input("Введите дату начала показа коллекции (1 - отмена): ").strip()
#        if start_time == "1":
#            return
#        data.append(start_time)
#
#        end_time = input("Введите дату окончания показа коллекции (1 - отмена): ").strip()
#        if end_time == "1":
#            return
#        data.append(end_time)
#
#        self.tables["Collections"].insert_one(data)

    def show_items_by_collection(self):
        obj = None
        while True:
            num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
            while len(num.strip()) == 0:
                num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
            if num == "0":
                return "1"
            try:
                collection = self.tables["Collections"].find_by_id(int(num))
                obj = collection
                break
            except Exception as e:
                print("Неверный порядковый номер!")

        print("Выбрана коллекция: " + obj[1])
        print("Экспонаты:")
        lst = self.tables["Items"].all_by_coll_id(num)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр коллекций;
    6 - добавление нового экспоната;
    7 - удаление экспоната;
    9 - выход."""
        print(menu)
        return self.read_next_step()


    def main_cycle(self):
        self.db_init()
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_collections()
                next_step = self.read_next_step()
                current_menu = self.after_show_collections(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_collection()
                current_menu = "1"
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# m.test()
m.main_cycle()
    

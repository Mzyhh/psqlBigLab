# import sys
# sys.path.append('tables')
from rich.console import Console
from rich.table import Table
import numpy as np

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
        self.tables = {
            'Halls':  Halls(),
            'Collections': Collections(),
            'Hazard': Hazard(),
            'Items': Items(),
            'Prices': Prices(),
            'PricesXCollections': PricesXCollections(),
        }
        

    def db_init(self):
        print("db_init()")
        for table in self.tables.values():
            table.create()

    def db_insert_somethings(self):
        print("db_insert_somethings()")
        ...

    def db_drop(self):
        print("db_drop()")
        for table in self.tables.values():
            table.drop()

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
            self.db_init()
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
        for name, style in zip(self.tables["Collections"].ru_column_names(), COLORS):
            table.add_column(name, style=style)

        for record in self.tables["Collections"].all():
            table.add_row(*[str(x) for x in record])
        self.console.print(table)

        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - просмотр телефонов человека;
    9 - выход."""
        print(menu)

    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                print("Пока не реализовано!")
                return "1"
            elif next_step == "6" or next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_collection(self):
        data = []

        max_len = 32 # TODO: remove 'magic' constant
        name = input("Введите название (1 - отмена): ").strip()
        if name == "1":
            return
        while (isempty := len(name) == 0) or len(name) > max_len:
            if isempty:
                name = input("Имя не может быть пустым! Введите имя заново (1 - отмена):").strip()
            else:
                name = input(f"Слишком длинное имя (максимум {max_len} символа) (1 - отмена):").strip()
            if name == "1":
                return
        data.append(name)

        max_len = 512
        description = input("Введите описание (1 - отмена): ").strip()
        if description == "1":
            return
        while (isempty := len(description) == 0) or len(description) > max_len:
            if isempty:
                description = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
            else:
                description = input(f"Слишком длинное описание (максимум {max_len} символов (1 - отмена)):").strip()
            if description == "1":
                return
        data.append(description)

        start_time = input("Введите дату начала показа коллекции (1 - отмена): ").strip()
        if start_time == "1":
            return
        data.append(start_time)

        end_time = input("Введите дату окончания показа коллекции (1 - отмена): ").strip()
        if end_time == "1":
            return
        data.append(end_time)

        self.tables["Collections"].insert_one(data)

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
                else:
                    self.person_id = int(person[1])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[2] + " " + self.person_obj[0] + " " + self.person_obj[3])
        print("Телефоны:")
        lst = PhonesTable().all_by_person_id(self.person_id)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового телефона;
    7 - удаление телефона;
    9 - выход."""
        print(menu)
        return self.read_next_step()

        return self.read_next_step()

    def main_cycle(self):
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
                current_menu = self.after_show_people(next_step)
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
    

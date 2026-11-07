import prompt
from . import core, utils
import shlex

def run():

    print("\n***База данных***")
    print("")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")

    while True:
        command = shlex.split(prompt.string("Введите команду: "))

        if not command:
            continue

        metadata = utils.load_metadata("db_meta.json")

        if command[0] == "help":
            if len(command) != 1:
                print(f"Неверное число аргументов для команды {command[0]}.")
                continue
            print_help()
            continue

        elif command[0] == "create_table":
            if len(command) < 2:
                print(f"Неверное число аргументов для команды {command[0]}.")
                continue
            
            data = core.create_table(metadata, command[1], command[2:])
            if data[1]:
                print(f'Таблица "{command[1]}" успешно создана со столбцами: {", ".join(data[0][command[1]])}')
                utils.save_metadata("db_meta.json", data[0])
            continue

        elif command[0] == "list_tables":
            if len(command) != 1:
                print(f"Неверное число аргументов для команды {command[0]}.")
                continue

            if not metadata:
                print("Таблиц нет.")
                continue
        
            for table in metadata:
                print("-", table)
            continue

        elif command[0] == "drop_table":
            if len(command) != 2:
                print(f"Неверное число аргументов для команды {command[0]}.")
                continue

            data = core.drop_table(metadata, command[1])
            if data[1]:
                print(f'Таблица "{command[1]}" успешно удалена.')
                utils.save_metadata("db_meta.json", data[0])
            continue

        elif command[0] == "exit":
            if len(command) != 1:
                print(f"Неверное число аргументов для команды {command[0]}.")
                continue
            break

        else:
            print(f"Функции {command[0]} нет. Попробуйте снова.")
            continue



def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 
import shlex

import prompt
from prettytable import PrettyTable

from . import core, utils


def run():

    print("\n***База данных***")
    print_help()

    while True:

        try:
            command = shlex.split(prompt.string("Введите команду: "))
        except ValueError:
            print("Ошибка ввода. Попробуйте снова.")
            continue
        
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
                print(
                f'Таблица "{command[1]}" успешно создана со столбцами: '
                f'{", ".join(data[0][command[1]])}'
                )
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

        elif command[0:2] == ["insert", "into"]:

            if len(command) < 4:
                    print("Неверные аргументы для команды insert into.")
                    continue
            
            if command[2] not in metadata:
                print(f"Таблицы {command[2]} не существует.")
                continue
            
            wr = core.insert(metadata, command[2], command[3:])

            if wr[1]:
                print(
                    f'Запись с ID={wr[2]} '
                    f'успешно добавлена в таблицу "{command[2]}".'
                    )
                utils.save_table_data(command[2], wr[0])
            continue

        elif command[0:2] == ["select", "from"]:

            if len(command) < 3:
                    print("Неверные аргументы для команды select from.")
                    continue
            
            if command[2] not in metadata:
                print(f"Таблицы {command[2]} не существует.")
                continue

            table_data = utils.load_table_data(command[2])
            where_clause_select = None

            if "where" in command:
                where_clause_select = parser(command, "where", command[2], metadata)
                if where_clause_select == {}:
                    print("Неверные аргументы для команды select from.")
                    continue

            result = core.select(table_data, where_clause_select)
            names = [c.split(":")[0] for c in metadata[command[2]]]
            pt = PrettyTable()
            pt.field_names = names
            for record in result:
                pt.add_row([record[name] for name in names])
            print(pt)
            continue

        elif command[0] == "update":

            if len(command) < 6:
                    print("Неверные аргументы для команды update.")
                    continue

            if len(command) > 6:
                print(f'Неверное число аргументов для команды "{command[0]}"')
                continue
            
            if command[1] not in metadata:
                print(f"Таблицы {command[1]} не существует.")
                continue   

            if command[2] != "set":
                print(f"Неверный аргумент {command[2]} для команды update.")
                continue

            update_set = parser(command, "set", command[1], metadata)
            if update_set == {}:
                print(f"Неверные аргументы {command[3]} для команды update.")
                continue

            if command[4] != "where":
                print(f"Неверный аргумент {command[4]} для команды update.")
                continue

            update_where = parser(command, "where", command[1], metadata)
            if update_where == {}:
                print(f"Неверные аргументы {command[5]} для команды update.")
                continue

            table_data = utils.load_table_data(command[1])
            update_table = core.update(table_data, update_set, update_where)
            if update_table[1]:
                print(f'Запись в таблице "{command[1]}" успешно обновлена.')
                utils.save_table_data(command[1], update_table[0])
            continue

        elif command[0:2] == ["delete", "from"]:

            if len(command) < 5:
                    print("Неверные аргументы для команды delete from.")
                    continue

            if len(command) > 5:
                print('Команда "delete from" может принимать не больше 1 значения.')
                continue
            
            if command[2] not in metadata:
                print(f"Таблицы {command[2]} не существует.")
                continue

            table_data = utils.load_table_data(command[2])

            if command[3] == "where":
                where_clause_delete = parser(command, "where", command[2], metadata)
            else:
                print(f'Неверный аргумент {command[3]} для команды "delete from".')
                continue

            res = core.delete(table_data, where_clause_delete)

            if res[1]:
                print(f'Запись с {command[4]} успешно '
                      f'удалена в таблице "{command[2]}".')
                utils.save_table_data(command[2], res[0])
            continue

        elif command[0] == "info":

            if len(command) < 2:
                    print("Неверные аргументы для команды info.")
                    continue

            if len(command) > 2:
                print(f'Неверное число аргументов для команды {command[0]}.')
                continue
            
            if command[1] not in metadata:
                print(f"Таблицы {command[1]} не существует.")
                continue

            table_data = utils.load_table_data(command[1])

            print(f"Таблица {command[1]}")
            print(f'Столбцы {", ".join(metadata[command[1]])}')
            print(f"Количество записей {len(table_data)}")
            continue
            
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

    print("\n***Операции с данными***")
    print("Команды вида 'a = b' обязательно заковываются в кавычки")
    print("<command> insert into <имя_таблицы> " \
    "values <значение1> <значение2> ... - создать запись.")
    print("<command> select from <имя_таблицы> where "
    "'<столбец> = <значение>' - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set " \
    "'<столбец1> = <новое_значение1>' where "
    "'<столбец_условия> = <значение_условия>' - обновить запись.")
    print("<command> delete from <имя_таблицы> " \
    "where '<столбец> = <значение>' - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 



def parser(command, keyword, table_name, metadata):

    d = {}
    i = command.index(keyword)

    if "=" not in command[i+1]:
        return d

    condition = command[i+1].split(" = ")
    k = condition[0]
    v = condition[1]

    for c in metadata[table_name]:
        if c.split(":")[0] != k:
            continue
        
        if c.split(":")[1] == "bool":
            if v.lower() not in ("true", "false"):
                print(f'Ошибка: аргумент {v} не соответствует типу bool.')
                return d
            else:
                if v.lower() == "true":
                    d[k] = True
                    return d
                else:
                    d[k] = False
                    return d
        elif c.split(":")[1] == "int":
            try:
                d[k] = int(v)
                return d
            except ValueError:
                print(f'Ошибка: аргумент {v} не соответствует типу int.')
                return d
        else:
            d[k] = v
            return d
        
    return d
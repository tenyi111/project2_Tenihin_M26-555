from pathlib import Path
from . import utils

def create_table(metadata, table_name, columns):

    success = False

    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata, success

    if not columns:
        print("Некорректное значение: столбцы не указаны. Попробуйте снова.")
        return metadata, success

    has_id = False

    for column in columns:

        if " " in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata, success

        words = column.split(":")

        if len(words) != 2:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata, success

        if words[0] == "" or words[1] not in ("str", "int", "bool"):
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata, success

        if words[0] == "ID":
            has_id = True
            if words[1] != "int":
                print(f"Некорректное значение: {column}. Попробуйте снова.")
                return metadata, success
    
    if has_id:
        if columns[0] != "ID:int":
                print(f"Ошибка: ID:int должен быть первым столбцом. Попробуйте снова.")
                return metadata, success
        table = columns.copy()
        metadata[table_name] = table
    else:
        table = ["ID:int"] + columns
        metadata[table_name] = table

    success = True

    return metadata, success



def drop_table(metadata, table_name):

    success = False

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata, success

    del metadata[table_name]
    success = True
    return metadata, success



def insert(metadata, table_name, values):

    success = False

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return [], success

    data = utils.load_table_data(table_name)

    if len(values) != len(metadata[table_name])-1:
        print('Ошибка: Количество аргументов не соответствует количеству аргументов таблицы, '
              f'"{table_name}" принимает {len(metadata[table_name])-1} аргументов.')
        return data, success

    IDs = []
    for record in data:
        IDs.append(record["ID"])
    
    it_id = max(IDs, default=0)+1

    row = {"ID":it_id}

    for value, column in zip(values, metadata[table_name][1:]):
        if column.split(":")[1] == "int":
            try:
                row[column.split(":")[0]] = int(value)
            except ValueError:
                print(f'Ошибка: аргумент {value} не соответствует типу {column.split(":")[1]}.')
                return data, success, it_id

        elif column.split(":")[1] == "bool":
            if value.lower() not in ("true", "false"):
                print(f'Ошибка: аргумент {value} не соответствует типу {column.split(":")[1]}.')
                return data, success, it_id
            else:
                if value.lower() == "true":
                    row[column.split(":")[0]] = True
                else:
                    row[column.split(":")[0]] = False

        else:
            row[column.split(":")[0]] = value

    data.append(row)
    utils.save_table_data(table_name, data)
    success = True
    return data, success, it_id



def select(table_data, where_clause=None):

    if where_clause is None:
        return table_data

    result = []

    for row in table_data:
        for column, value in where_clause.items():
            if column not in row:
                print(f'Ошибка: столбец "{column}" не существует.')
                return []
            if row[column] == value:
                result.append(row)

    return result



def update(table_data, set_clause, where_clause):

    success = False

    for row in table_data:
        for column, value in where_clause.items():
            if column not in row:
                print(f'Ошибка: столбец "{column}" не существует.')
                return table_data, success
            
            if row[column] == value:
                for col, v in set_clause.items():
                    if col not in row:
                        print(f'Ошибка: столбец "{col}" не существует.')
                        return table_data, success

                    if col == "ID":
                        print(f'Ошибка: столбец "ID" нельзя менять напрямую.')
                        return table_data, success
                    
                    row[col] = v
    success = True

    return table_data, success



def delete(table_data, where_clause):

    success = False

    result = table_data.copy()

    for row in table_data:
        for column, value in where_clause.items():
            if column not in row:
                print(f'Ошибка: столбец "{column}" не существует.')
                return table_data, success
            if row[column] == value:
                result.remove(row)
    success = True

    return result, success
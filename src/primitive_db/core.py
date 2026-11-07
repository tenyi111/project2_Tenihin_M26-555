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
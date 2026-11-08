import json
from pathlib import Path


def load_metadata(filepath):

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}



def save_metadata(filepath, data):

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)



def load_table_data(table_name):

    Path("data").mkdir(exist_ok=True)

    filepath = f"data/{table_name}.json"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []



def save_table_data(table_name, data):

    Path("data").mkdir(exist_ok=True)

    filepath = f"data/{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)
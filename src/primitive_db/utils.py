import json

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
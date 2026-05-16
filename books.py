import json
from collections import Counter

def load_books(filename='books.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            books = json.load(f)
        return books
    except FileNotFoundError:
        print(f'Файл {filename} не найден')
        return []
    except json.JSONDecodeError:
        print(f'Ошибка: файл {filename} повреждён')
        return []

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

def display_all_books(books):
    if not books:
        print('\nСписок книг пуст')
        return
    print('\n' + '='*60)
    print(f'ВСЕ КНИГИ (всего: {len(books)})')
    print('='*60)
    for i, book in enumerate(books, 1):
        title = book.get('title', 'Нет названия')
        author = book.get('author', 'Нет автора')
        rating = book.get('rating', 'Нет оценки')
        if rating != 'Нет оценки':
            print(f'{i}. "{title}" - {author} | Оценка: {rating}')
        else:
            print(f'{i}. "{title}" - {author}')
    print('='*60 + '\n')

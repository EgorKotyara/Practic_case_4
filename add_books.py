import json
import os
from datetime import datetime

def save_books(books, filename='books.json'):
    if not isinstance(books, list):
        print(f'Ошибка: попытка сохранить не список, а {type(books).__name__}')
        return False
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        print(f'Сохранено {len(books)} книг в файл {filename}')
        return True
    except PermissionError:
        print(f'Ошибка: нет прав для записи в файл {filename}')
        return False
    except Exception as e:
        print(f'Ошибка при сохранении: {e}')
        return False

def validate_rating():
    while True:
        rating_input = input('Введите оценку (1-5), q для отмены или оставьте пустым: ').strip()
        if rating_input.lower() == 'q':
            print('Добавление книги отменено пользователем')
            return 'CANCEL'
        if rating_input == '':
            return None
        try:
            rating_float = float(rating_input)
            if 1 <= rating_float <= 5:
                return rating_float
            print('Ошибка: оценка должна быть от 1 до 5')
        except ValueError:
            print('Ошибка: введите число, оставьте пустым или введите q для отмены')

def validate_date():
    while True:
        date_input = input('Введите дату прочтения (ГГГГ-ММ-ДД), q для отмены или оставьте пустым: ').strip()
        if date_input.lower() == 'q':
            print('Добавление книги отменено пользователем')
            return 'CANCEL'
        
        if date_input == '':
            return None
        try:
            datetime.strptime(date_input, '%Y-%m-%d')
            return date_input
        except ValueError:
            print('Ошибка: неверный формат даты. Используйте ГГГГ-ММ-ДД')

def is_duplicate(books, title, author):
    for book in books:
        if book.get('title', '').lower() == title.lower() and book.get('author', '').lower() == author.lower():
            return True
    return False

def add_books(filename='books.json'):
    books = load_books(filename)
    string = 'Введите название и автора книги через пробел или q для выхода'
    added_count = 0
    cancelled_count = 0
    while True:
        inp = input(f'\n{string}: ')
        if inp.lower() == 'q':
            break
        if not inp.strip():
            print('Ошибка: введите название и автора через пробел')
            continue
        try:
            parts = inp.split(maxsplit=1)
            if len(parts) != 2:
                print('Ошибка: нужно ввести название и автора через пробел')
                continue
            title, author = parts
            if is_duplicate(books, title, author):
                print(f'Ошибка: книга "{title}" автора {author} уже существует')
                continue
            print(f'\nКнига: "{title}" - {author}')
            rating = validate_rating()
            if rating == 'CANCEL':
                cancelled_count += 1
                continue
            date = validate_date()
            if date == 'CANCEL':
                cancelled_count += 1
                continue
            books.append({
                'title': title.strip(),
                'author': author.strip(),
                'rating': rating,
                'date': date
            })
            if save_books(books, filename):
                added_count += 1
                print(f'Книга "{title}" успешно добавлена!')
            else:
                print(f'Ошибка: книга "{title}" не была сохранена')
        except Exception as e:
            print(f'Неожиданная ошибка: {e}')

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

def calculate_average_rating(books):
    if not books:
        print("Список книг пуст, невозможно вычислить среднюю оценку")
        return None
    ratings = []
    books_with_ratings = 0
    for book in books:
        rating = book.get('rating')
        if rating is not None and isinstance(rating, (int, float)):
            ratings.append(rating)
            books_with_ratings += 1
        elif rating is not None and isinstance(rating, str):
            try:
                numeric_rating = float(rating)
                ratings.append(numeric_rating)
                books_with_ratings += 1
            except ValueError:
                pass
    if not ratings:
        print('\nНет книг с оценками для расчёта средней')
        return None
    average = sum(ratings) / len(ratings)
    print('\n' + '='*60)
    print('СТАТИСТИКА ОЦЕНОК')
    print('='*60)
    print(f'Всего книг: {len(books)}')
    print(f'Книг с оценками: {books_with_ratings}')
    print(f'Сумма всех оценок: {sum(ratings):.1f}')
    print(f'Средняя оценка: {average:.2f}')
    print(f'Минимальная оценка: {min(ratings):.1f}')
    print(f'Максимальная оценка: {max(ratings):.1f}')
    print('='*60 + '\n')
    return average

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
        rating = book.get('rating')
        if rating is not None:
            print(f'{i}. "{title}" - {author} | Оценка: {rating}')
        else:
            print(f'{i}. "{title}" - {author}')
    print('='*60 + '\n')

def calculate_average_rating(books):
    if not books:
        print("Список книг пуст, невозможно вычислить среднюю оценку")
        return None
    ratings = []
    for book in books:
        rating = book.get('rating')
        if rating is None:
            continue
        try:
            numeric_rating = float(rating)
            if 1 <= numeric_rating <= 5:
                ratings.append(numeric_rating)
        except (ValueError, TypeError):
            pass
    if not ratings:
        print('\nНет книг с корректными оценками для расчёта средней')
        return 
    average = sum(ratings) / len(ratings)
    print('\n' + '='*60)
    print('СТАТИСТИКА ОЦЕНОК')
    print('='*60)
    print(f'Всего книг: {len(books)}')
    print(f'Книг с оценками: {len(ratings)}')
    print(f'Сумма всех оценок: {sum(ratings):.1f}')
    print(f'Средняя оценка: {average:.2f}')
    print(f'Минимальная оценка: {min(ratings):.1f}')
    print(f'Максимальная оценка: {max(ratings):.1f}')
    print('='*60 + '\n')
    return average

def author_statistic(books):
    if not books:
        print('\nСписок книг пуст')
        return {}
    author_counts = Counter()
    for book in books:
        author = book.get('author', 'Неизвестный автор')
        author_counts[author] += 1
    print('\n' + '='*60)
    print('СТАТИСТИКА ПО АВТОРАМ')
    print('='*60)
    print(f'Всего авторов: {len(author_counts)}')
    print(f'Всего книг: {sum(author_counts.values())}')
    print('-'*60)
    sorted_authors = sorted(author_counts.items(), key=lambda x: (-x[1], x[0]))
    for i, (author, count) in enumerate(sorted_authors, 1):
        if count == 1:
            book_word = 'книга'
        elif 2 <= count <= 4:
            book_word = 'книги'
        else:
            book_word = 'книг'
        print(f'{i}. {author}: {count} {book_word}')
    print('='*60 + '\n')
    return dict(author_counts)

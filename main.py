import json
import os
from datetime import datetime
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

def save_books(books, filename='books.json'):
    if not isinstance(books, list):
        print(f'Ошибка: попытка сохранить не список, а {type(books).__name__}')
        return False
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
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
        date_input = input('Введите дату прочтения (ДД-ММ-ГГГГ), q для отмены или оставьте пустым: ').strip()
        if date_input.lower() == 'q':
            print('Добавление книги отменено пользователем')
            return 'CANCEL'
        
        if date_input == '':
            return None
        try:
            datetime.strptime(date_input, '%d-%m-%Y')
            return date_input
        except ValueError:
            print('Ошибка: неверный формат даты. Используйте ДД-ММ-ГГГГ')

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
        date = book.get('date')
        if rating is not None:
            print(f'{i}. "{title}" - {author} | Оценка: {rating} | Дата прочтения: {date}')
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

def delete_by_index(books, index):
    if 1 <= index <= len(books):
        removed_book = books.pop(index - 1)
        print(f'Книга "{removed_book["title"]}" автора {removed_book["author"]} удалена')
        return True, removed_book
    else:
        print(f'Ошибка: индекс {index} вне диапазона (1-{len(books)})')
        return False, None

def delete_by_title_author(books, title, author):
    removed_books = []
    for i in range(len(books) - 1, -1, -1):
        if (books[i]['title'].lower() == title.lower() and 
            books[i]['author'].lower() == author.lower()):
            removed_books.append(books.pop(i))
    
    if removed_books:
        for book in removed_books:
            print(f'Книга "{book["title"]}" автора {book["author"]} удалена')
        return True, removed_books
    else:
        print(f'Книга "{title}" автора {author} не найдена')
        return False, None

def delete_book(filename='books.json'):
    books = load_books(filename)
    if not books:
        print('Нет книг для удаления')
        return False
    print('\nТекущий список книг:')
    for i, book in enumerate(books, 1):
        rating_info = f" (оценка: {book['rating']})" if book.get('rating') else ''
        print(f'{i}. "{book["title"]}" - {book["author"]}{rating_info}')
    print('\nВыберите способ удаления:')
    print('1. По индексу (номеру) в списке')
    print('2. По названию и автору')
    print('3. Отмена')
    choice = input('\nВаш выбор (1-3): ')
    if choice == '1':
        try:
            index = int(input(f'Введите номер книги для удаления (1-{len(books)}): '))
            success, _ = delete_by_index(books, index)
            if success:
                return save_books(books, filename)
            return False
        except ValueError:
            print('Ошибка: введите число')
            return False
    elif choice == '2':
        title = input('Введите название книги: ').strip()
        author = input('Введите автора книги: ').strip()
        if not title or not author:
            print('Ошибка: название и автор не могут быть пустыми')
            return False
        success, _ = delete_by_title_author(books, title, author)
        if success:
            return save_books(books, filename)
        return False
    elif choice == '3':
        print('Удаление отменено')
        return False
    else:
        print('Неверный выбор')
        return False

def main():
    filename = 'books.json'
    while True:
        print('\n' + '='*60)
        print('МЕНЮ БИБЛИОТЕКИ')
        print('='*60)
        print('1. Добавить книгу')
        print('2. Показать все книги')
        print('3. Показать среднюю оценку')
        print('4. Статистика по авторам')
        print('5. Удалить книгу')
        print('6. Выход')
        print('='*60)
        
        choice = input('Выберите действие (1-6): ')
        
        if choice == '1':
            add_books(filename)
        elif choice == '2':
            books = load_books(filename)
            display_all_books(books)
        elif choice == '3':
            books = load_books(filename)
            calculate_average_rating(books)
        elif choice == '4':
            books = load_books(filename)
            author_statistic(books)
        elif choice == '5':
            delete_book(filename)
        elif choice == '6':
            print('До свидания!')
            break
        else:
            print('Неверный выбор. Пожалуйста, выберите 1-6')

if __name__ == "__main__":
    main()
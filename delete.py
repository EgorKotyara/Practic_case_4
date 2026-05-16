import json

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
    from book_utils import load_books, save_books
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

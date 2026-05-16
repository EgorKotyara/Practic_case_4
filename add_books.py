def add_books(books):
  string = 'Введите название и автора книги через пробел или q для выхода'
  while True:
    inp = input(string)
    if inp == 'q':
      break
    try:
      title, author = inp.split(maxsplit=1)
      books.append({
        'title': title,
        'author': author
      })
      print(f'Книга: {title}, автор: {author} добавлена')
    except ValueError:
      print('Повторите ввод или введите q для выхода')
      

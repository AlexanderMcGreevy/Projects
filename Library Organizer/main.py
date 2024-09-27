#Library Organizer Project
from datetime import date, timedelta
#Saves the date 30 days from now for borrowing return date
days30 = (date.today() + timedelta(days=30)).isoformat()


#Manages book info
class Library:

  def __init__(self):
    self.size = 10000
    self.table = [[] for _ in range(self.size)]

  def store(self, title, author):
    index = self.get_hash(title)

    # File book storage for easy listing
    present = False
    with open('/workspaces/Projects/Library Organizer/books.txt', 'r') as file:
      for line in file:
        if title in line:
          present = True
          break

    if not present:
      self.table[index].append([title, author, 'available'])
      with open('/workspaces/Projects/Library Organizer/books.txt', 'a') as file:
        file.write('\n' + title + ',' + author + ',' + 'available')
      print(f"Book {title} added to the library")
    else:
      print(f"Book {title} already exists")

  #Gets Book Data from the Hashtable
  def get(self, title):
    index = self.get_hash(title)
    for var in self.table[index]:
      if var[0] == title:
        return var[1]
    return None

  #Removes the book from both the file and hashtable
  def remove(self, title):
    #Removes from file
    with open('/workspaces/Projects/Library Organizer/books.txt', 'r') as file:
      lines = file.readlines()
    with open('/workspaces/Projects/Library Organizer/books.txt', 'w') as file:
      for line in lines:
        if title not in line:
          file.write(line)
      print(f"Book {title} removed")
    #Removes from hash
    index = self.get_hash(title)
    for i, var in enumerate(self.table[index]):
      if var[0] == title:
        del self.table[index][i]
        break

  #Gets the hash of the book info
  def get_hash(self, key):
    return hash(key) % self.size

  #Changes status of library book and adds it to user account
  def borrow(self, account, book):
    available = False
    with open('/workspaces/Projects/Library Organizer/books.txt', 'r') as file:
      lines = file.readlines()
    with open('/workspaces/Projects/Library Organizer/books.txt', 'w') as file:
      for line in lines:
        if book not in line:
          file.write(line)
        elif book in line:
          if 'borrowed' in line:
            break
          elif 'available' in line:
            file.write(line.replace('available', 'borrowed'))
            available = True
            print(f"Please return {book} by {days30}")
    #Changes status to borrowed within the library system
    if available:
      index = library.get_hash(book)
      for i, var in enumerate(library.table[index]):
        if var[0] == book:
          library.table[index][i][2] = 'borrowed'
      with open('/workspaces/Projects/Library Organizer/accounts.txt', 'r') as file:
        lines = file.readlines()
      with open('/workspaces/Projects/Library Organizer/accounts.txt', 'w') as file:
        for line in lines:
          if account.name not in line:
            file.write(line)
          elif account.name in line:
            file.write(line + f",{book}")

    #Returns a book to the library
  def return_book(self, account, book):
    available = False
    with open('/workspaces/Projects/Library Organizer/books.txt', 'r') as file:
      lines = file.readlines()
    with open('/workspaces/Projects/Library Organizer/books.txt', 'w') as file:
      for line in lines:
        if book not in line:
          file.write(line)
        if book in line:
          file.write(line.replace('borrowed', 'available'))
          available = True
    if available:
      index = library.get_hash(book)
      for i, var in enumerate(library.table[index]):
        if var[0] == book:
          library.table[index][i][2] = 'available'
      with open('/workspaces/Projects/Library Organizer/accounts.txt', 'r') as file:
        lines = file.readlines()
      with open('/workspaces/Projects/Library Organizer/accounts.txt', 'w') as file:
        for line in lines:
          if account.name not in line:
            file.write(line)
          if account.name in line:
            file.write(line.replace(f",{book}", ""))
    print('You have returned the book')


#Account Functions
class Account:

  def __init__(self, name, password):
    self.name = name
    self.password = password

  def viewAccount(self):
    with open('/workspaces/Projects/Library Organizer/accounts.txt', 'r') as file:
      accounts = [line.strip().split(',') for line in file.readlines()]
    for acc in accounts:
      if self.name == acc[0]:
        books = acc[2:]

    print('\nName:', self.name, '\n')
    print('Books:', books, '\n')


#View all books in the library
def viewBooks():
  print('\nBooks: ')
  with open('/workspaces/Projects/Library Organizer/books.txt', 'r') as file:
    print(file.read())
  menu()


def donateBook():
  title = input('Enter the title of the book: ')
  author = input('Enter the author of the book: ')
  library.store(title, author)
  menu()


#Removes all duplicate files
def checkFiles():
  with open('/workspaces/Projects/Library Organizer/books.txt', 'r') as file:
    lines = file.readlines()
    newl = ''
  with open('/workspaces/Projects/Library Organizer/books.txt', 'w') as file:
    for line in lines:
      if line not in newl:
        newl += line
    file.write(newl)
  with open('/workspaces/Projects/Library Organizer/accounts.txt', 'r') as file:
    lines = file.readlines()
    newl = ''
  with open('/workspaces/Projects/Library Organizer/accounts.txt', 'w') as file:
    for line in lines:
      if line not in newl:
        newl += line
    file.write(newl)


def login():
  new = input('Would You like to (1)Login or (2)Create an account?: ')
  if new == '2':
    name = input('Enter your username: ')
    password = input('Enter your password: ')
    with open('/workspaces/Projects/Library Organizer/accounts.txt', 'r') as file:
      accounts = [line.strip().split(',') for line in file.readlines()]
    for acc in accounts:
      if name == acc[0]:
        print("Account already exists")
        return None
    with open('/workspaces/Projects/Library Organizer/accounts.txt', 'a') as file:
      file.write(f"\n{name},{password}")
    account = Account(name, password)
    return account
  elif new == '1':
    name = input('Enter your username: ')
    passw = input('Enter your password: ')
    with open('/workspaces/Projects/Library Organizer/accounts.txt', 'r') as file:
      accounts = [line.strip().split(',') for line in file.readlines()]
    for acc in accounts:
      if name == acc[0] and passw == acc[1]:
        return Account(name, passw)
    return None


def menu():
  ans = input(
      '\n\033[1mLibrary Access Terminal\033[0m\n\n(1)Login\n(2)View Available Books\n(3)Donate Book\n(4)Exit\n\nEnter your choice: '
  )
  if ans == '1':
    account = login()
    if account:
      print(f"\nWelcome, {account.name}!")
      x = input(
          f'\nWould You like to (1)View Account, (2)Borrow Book, (3)Return Book, or (4) Return to Menu?: '
      )
      if x == '1':
        account.viewAccount()
      elif x == '2':
        book = input("\nEnter the title of the book you want to borrow: ")
        library.borrow(account, book)
      elif x == '3':
        book = input("\nEnter the title of the book you want to return: ")
        library.return_book(account, book)
    else:
      print("Invalid username or password.")
    menu()
  elif ans == '2':
    viewBooks()
  elif ans == '3':
    donateBook()


#Creates an object for the Library
library = Library()

#Unit Tests/Library File setup
library.store('The Hobbit', 'JRR Tolkein')
library.store('The Lord of the Rings', 'JRR Tolkein')
print(library.get('The Hobbit'))
library.remove('The Hobbit')
print(library.get('The Hobbit'))
library.store('The Hobbit', 'JRR Tolkein')
library.store('Ready Player One', 'Ernest Cline')
library.store('The Hunger Games', 'Suzanne Collins')
library.store('The Lion, the Witch and the Wardrobe', 'C.S. Lewis')
library.store("Harry Potter and the Philosopher's Stone", 'J.K. Rowling')
library.store('Game of Thrones', 'George R.R. Martin')
library.store('1984', 'George Orwell')
library.store("The Hitchhiker's Guide to the Galaxy", 'Douglas Adams')
library.store('The Girl with the Dragon Tattoo', 'Stieg Larsson')
library.store('Moby-Dick', 'Herman Melville')
library.store('Pride and Prejudice', 'Jane Austen')
library.store('To Kill a Mockingbird', 'Harper Lee')
library.store('The Catcher in the Rye', 'J.D. Salinger')
library.store('Brave New World', 'Aldous Huxley')
library.store('The Great Gatsby', 'F. Scott Fitzgerald')
library.store('One Hundred Years of Solitude', 'Gabriel García Márquez')

checkFiles()

menu()

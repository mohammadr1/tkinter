from tkinter import *

class Book:
    def __init__(self, title, author, price, stock):
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

class BookStoreManagement:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def sell_book(self, book_title):
        for book in self.books:
            if book.title == book_title:
                if book.stock > 0:
                    book.stock -= 1
                    print(f"{book_title} sold successfully!")
                else:
                    print(f"Sorry, {book_title} is out of stock.")
                return
        print(f"Book '{book_title}' not found in the bookstore.")

    def search_books(self, query):
        found_books = []
        for book in self.books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                found_books.append(book)
        return found_books

    def generate_sales_report(self):
        total_sold_books = sum(book.stock for book in self.books)
        total_revenue = sum(book.price for book in self.books if book.stock < book.stock)
        print("Sales Report:")
        print(f"Total sold books: {total_sold_books}")
        print(f"Total revenue: {total_revenue}")

# یک نمونه از کتابفروشی بسازیم
bookstore = BookStoreManagement()

# اضافه کردن چند کتاب به کتابفروشی
book1 = Book("Title 1", "Author 1", 10, 5)
book2 = Book("Title 2", "Author 2", 15, 10)
book3 = Book("Title 3", "Author 3", 20, 3)
bookstore.add_book(book1)
bookstore.add_book(book2)
bookstore.add_book(book3)

# برخی عملیات از طریق رابط کاربری
print(bookstore.search_books("title"))
bookstore.sell_book("Title 1")
bookstore.sell_book("Title 1")
bookstore.sell_book("Title 4")
bookstore.generate_sales_report()
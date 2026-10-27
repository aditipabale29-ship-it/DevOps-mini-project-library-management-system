from datetime import date

from app.models.book import Book
from app.models.user import User
from app.models.loan import Loan


class LibraryService:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.loans = {}
        self.next_book_id = 1
        self.next_user_id = 1
        self.next_loan_id = 1

    def add_book(self, title, author, isbn, copies=1):
        book = Book(self.next_book_id, title, author, isbn, copies)
        self.books[self.next_book_id] = book
        self.next_book_id += 1
        return book.to_dict()

    def add_user(self, name, email, role="Student"):
        user = User(self.next_user_id, name, email, role)
        self.users[self.next_user_id] = user
        self.next_user_id += 1
        return user.to_dict()

    def borrow_book(self, book_id, user_id):
        book = self.books.get(book_id)
        user = self.users.get(user_id)

        if book is None:
            return {"error": "Book not found"}

        if user is None:
            return {"error": "User not found"}

        if book.copies <= 0:
            return {"error": "No copies available"}

        book.copies -= 1
        user.active_loans += 1

        loan = Loan(
            self.next_loan_id,
            book_id,
            user_id,
            date.today().isoformat()
        )
        self.loans[self.next_loan_id] = loan
        self.next_loan_id += 1

        return loan.to_dict()

    def return_book(self, loan_id):
        loan = self.loans.get(loan_id)

        if loan is None:
            return {"error": "Loan not found"}

        if loan.return_date is not None:
            return {"error": "Book already returned"}

        loan.return_date = date.today().isoformat()
        self.books[loan.book_id].copies += 1
        self.users[loan.user_id].active_loans -= 1

        return loan.to_dict()

    def list_books(self):
        return [book.to_dict() for book in self.books.values()]

    def list_users(self):
        return [user.to_dict() for user in self.users.values()]

    def list_loans(self):
        return [loan.to_dict() for loan in self.loans.values()]

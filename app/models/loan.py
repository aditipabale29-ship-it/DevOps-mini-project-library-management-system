class Loan:
    def __init__(self, loan_id, book_id, user_id, borrow_date, return_date=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date
        }

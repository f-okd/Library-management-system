import database

# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

'''

bookreturn.py module has one function return_book(book_id) which takes in a book id and validates the input complies
with standards. It then checks that the book isn't already available for return. After all this has been checked the log
is updated and the return date is set to present date and the member's name is removed from the book entry in database.txt.

'''


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


def return_book(book_id):

    # Tests if input is numeric, even if a string is entered, this will also catch negative numbers
    if not book_id.isnumeric():
        return "ERROR: Book ID must be numeric"

    # Tests if the book id exists in the database, so if you enter a number too large it should be flagged as an error
    elif int(book_id) > len(database.db):
        return "ERROR: This book does not exist"

    # if the book is available for checkout, error is returned
    elif database.available(book_id):
        return "ERROR: Book is already available, it can't be returned"

    else:
        # get the entire book entry, if the id matches
        book = [bbook for bbook in database.db if bbook[0] == book_id][0]

        # if book is overdue return warning message
        if database.overdue(book):
            database.book_return(book_id)
            return "Book successfully returned\nWARNING: BOOK WAS OVERDUE"
        else:
            database.book_return(book_id)
            return "Book successfully returned"


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#



if __name__ == '__main__':

    # 1
    # Validates that only positive numeric inputs are accepted
    print("1a", return_book("a"))
    print("1b", return_book("-4"))

    # 2
    # Validates that you can not return a book that is already available for checkout
    print("2", return_book("23"))

    # 3
    # Validates that the book exists in the database, if you enter anything > 48, should return an error
    print("3",return_book("999"))

    """
#commented out as it can only be run once without changing the status of the book

FUNCTIONALITY TESTING
---------------------
    print(return_book("42"))

    # Tests that a warning message is displayed when an overdue book is returned
    print(return_book("17")

"""
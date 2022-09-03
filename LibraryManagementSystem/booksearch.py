
import database

# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#

'''

booksearch.py module has one function search_title(title) that takes in a string as a title and returns a list of books 
which match the current input. It returns this alongside a boolean value representing whether a book is overdue or not.

'''

# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


def search_title(title):
    books = []
    len_title = len(title)

    # for every book in the database...
    for book in database.db:

        # if the title (2nd attribute of book type) (as far as the user has typed) is the same as the desired book then...
        # It also returns the overdue status with it as a tuple, this is used as a tag in the menu treeview
        if (book[2]).lower()[:len_title] == title.lower():
            books.append((book, database.overdue(book)))

    return books


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    
    # 1
    # Validates functionality -> should return list of tuples containing list of book attributes and overdue status
    print("1",search_title("Ender's game"))
    

    # 2
    # Validates that input is not case sensitive
    # Validates that the function collects multiple entries of the same book title
    print("2",search_title("BROWN GIRL IN THE RING"))
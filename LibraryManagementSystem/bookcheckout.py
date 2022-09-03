import database
# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

'''

bookcheckout.py module has one function withdraw(member_id, book_id).
withdraw takes in a member id and book id and validates that the inputs are appropriate. After input validation it calls
the checkout function in database.py module and updates the database with the member id as the new borrower of that 
book. A log entry is generated with present date as the checkout date, and 0 as return date, and the member id is next to 
entry.

'''

# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

def withdraw(member_id, book_id):

    # check if member id is 4char long
    if len(member_id) == 4:
        # check if member id only has characters
        if not member_id.isalpha():
            return "ERROR: Member ID can only contain letters"
    else:
        return "ERROR: Member ID must be 4 characters long"

    # check if book id is a number
    if not book_id.isnumeric():
        return "ERROR: Book ID must be a number"

    # check if book id is out of range (too large)
    elif int(book_id) > len(database.db):
        return "ERROR: This book does not exist"

    # check the book is not currently on loan to someone else
    elif database.available(book_id):
        database.checkout(member_id, book_id)
        return "Book successfully checked out"
    else:
        return "Book is on loan to someone else"

# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    
    #1
    # Validates that member ID can only contain letters
    print("1",withdraw("1234", 1))

    # 2
    # Validates that Member ID can only be 4 characters long
    print("2",withdraw("abcde", 1))
    
    # 3
    # Validates that book id must be a number
    print("3",withdraw("abcd", "a"))

    # 4
    # Validates that the function won't let a user checkout a book on loan to someone else
    print("4", withdraw("abcd", "1"))

    # Validates that the book exists in the database, if you enter anything > 48, should return an error
    #5
    # Validates that book id must be within range, 
    # There are only 48 database entries so any input > 48 returns an error
    print("5",withdraw("abcd", "9999"))


"""
*commented out because it can only be run once before the status of the book is changed

FUNCTIONALITY TESTING:
--------------------
>> print(withdraw("abcd", "20"))
>> Book successfully checked out
* Database is updated with abcd next to book 20 entry
* Log entry is generated with present date as the checkout date (13/12..), 0 as return date, abd "abcd" is next to entry
"""
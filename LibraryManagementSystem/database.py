from datetime import datetime  # will be used for date calculation

db = [] 
log = []


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------CREATING COPIES OF LOG HISTORY AND DATABASE-----------------------------------#
# --------------------------------------------------------------------------------------------------------------------=#


''' 

The purpose of the update function makes it so that after data is accessed or changed in the text files the local copies 
stored in 'db' and 'log' are set to the values in the text files.

'''


def update():

    book_database = open("database.txt", "r")

    logfile = open("logfile.txt", "r")

    while True:
        line = book_database.readline()
        if line == "":  # when you reach the end of the file
            break
        # want to remove the \n from the line
        line = line.strip()
        # each attribute of every book divided by commas,
        # by splitting each book is processed as a list of these attributes
        line = line.split(",")
        db.append(line)  # add this new book (divided by its attributes) into our database

    # similarly, with the database, will populate a list containing all the log history
    while True:
        line = logfile.readline()
        if line == "": 
            break
        line = line.strip()
        line = line.split(",")
        log.append(line)
    
    # stop wasting memory we have already made local copies of the database
    book_database.close()
    logfile.close()


update()
# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------CHECK IF A BOOK IS OVERDUE-------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


'''

Overdue function cycles through the log file and compares book checkout dates with the present date if the difference 
between the two dates is greater than 60 days then the book is added to a list of overdue books. The overdue function 
takes a book arguement and checks if that book's id is in the list of overdue books and returns a boolean value 
accordingly.

'''


def overdue(book):

    overdue_books = []

    # specifying how we want the time data to be formatted
    date_format = "%d/%m/%Y"

    for i in range(len(log)):
        # store id of current book
        book_id = log[i][1]
        book_id = int(book_id)
        checkout_date = log[i][2]
        # strip date values from string based on earlier specified format
        checkout_date = datetime.strptime(checkout_date, date_format)
        # if the book hasn't been returned yet

        if log[i][3] == "0":
            return_date = datetime.today()
            # creates delta for elapsed time
            delta = return_date - checkout_date
            # days is an attribute of all time deltas -> process the elapsed time as days, if its >60 then highlight it

            if delta.days > 60:
                # store book's id
                book_id = log[i][1]
                # for all books in the database

                for x in db:
                    # if the book id matches that of the identified overdue book

                    if x[0] == book_id:
                        # create list of overdue books
                        overdue_books.append(x)

    # returns true/false for if book is overdue or not
    return book in overdue_books


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------CHECK IF BOOK IS AVAILABLE----------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


'''

Available function takes in a book id and checks in the database for a book with a matching number id as the input.
It then checks that the field in the database where the member id is states is empty (has a 0). If so the book is 
available, otherwise it isn't.

'''


def available(book_id):

    for i in db:

        # if the book id matches that of the one being queried
        if i[0] == book_id:

            # if the book currently isn't on loan
            if i[5] != "0":
                return False
            else:
                return True


# ---------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------CHECK OUT BOOK---------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


'''

Checkout function takes in a member id and a book id, it finds the corresponding book in the database and creates a new
entry in the local log file 'log'. It sets the checkout date to present date and the return date to zero and also it 
puts the name of the member withdrawing the book in that entry. It also updates the local database 'db' by setting the 
member id as the one in the argument. 

Once the local database and log file are updated they are then written back into the textfile to make the changes 
permanent. Then the update function is called again.

'''


def checkout(member_id, book_id):

    # for all elements in the database
    for i in db:

        # if the book id matches the queried id
        if i[0] == book_id:
            # update this id to be the new id
            i[5] = member_id

    log.append([str(len(log)), book_id, datetime.today().strftime('%d/%m/%Y'), "0", member_id])
    
    f = open("database.txt", "w")

    for i in db:
        # will concatenate all elements(i = books) in db with a comma
        # remember all elements in db are formatted as: [id,genre,title,author,date of purchase,member in possession])
        i = ','.join(i)
        # we are going to write it back into the file, so we want each book to be written on a new line
        i = i+"\n"
        f.write(i)
    f.close()

    logfile = open("logfile.txt", "w")

    for i in log:
        i = ','.join(i) 
        i = i+"\n" 
        logfile.write(i)
    logfile.close()

    # reset stored db in python
    globals()["db"] = []
    globals()["log"] = []
    # want to create a local db again, so we can keep operating on it as a list
    update()

# ---------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------RETURN BOOK---------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


'''

book_return(book_id) function takes in a book id and checks the local log, 'log', to find a book which has the return 
date set as 0 and also has a matching book id as the one passed in argument then the return date is set to present date.
Then it finds the corresponding book in the local database, 'db', and sets the member id to 0 because it is no longer on
loan to anyone. Local lists 'db' and 'log' are then written back into text file to make changes permanent, then update 
function is called again.

'''


def book_return(book_id):

    for logs in log:
        # if the book is unreturned, and it matches the queried book id (the one we are trying to return)
        if (logs[3] == "0") and (logs[1] == book_id):
            today = datetime.today().strftime('%d/%m/%Y')
            logs[3] = today

            # update database to change
            for book in db:

                if book[0] == book_id:
                    book[5] = "0"

    logfile = open("logfile.txt", "w")

    for a_log in log:
        a_log = ','.join(a_log) 
        a_log = a_log+"\n" 
        logfile.write(a_log)

    book_database = open("database.txt", "w")

    for i in db:
        i = ','.join(i)
        i = i+"\n"
        book_database.write(i)

    logfile.close()

    book_database.close()

    # reset stored db in python
    globals()["db"] = []
    globals()["log"] = []

    # want to create a local db again, so we can keep operating on it as a list
    update()

# ---------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------GROUP RECORDS BASED ON ATTRIBUTES----------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


'''

When recommending books we want to be able to look at groups of books based on shared attributes like genre etc.
The history function takes in  a member_id and collects lists of all the books they have read. It returns a list of 
book ids for all the books the member has read and the id of the book they read last.

'''


def history(member_id):

    # store all books user has read, no duplicates
    read_books = []

    # store a log of books user reads in order (including duplicates)
    book_history = []

    for a_log in log:

        if a_log[4] == member_id:
            book_history.append(a_log[1])

    # convert list of read books into a dictionary to remove duplicates, then turn it back into a list
    read_books = list(dict.fromkeys(book_history))

    # get id of last book user read, if the list is empty then it just returns empty list
    last_read_book = book_history[-1:]

    return last_read_book, read_books


'''

Genre_list takes a book id and returns a list of book ids for all books of the same genre

'''


def genre_list(book_id):

    books_of_same_genre = []

    for book in db:

        # find the book in the database and record the genre
        if book[0] == book_id:
            genre = book[1]

    for book in db:

        # record all books of the same genre
        if book[1] == genre:
            books_of_same_genre.append(book[0])

    # return list of ids
    return books_of_same_genre


'''

most_popular_books returns a dictionary of all the books and how much they've been withdrawn.

'''


def most_popular_books():

    books_by_popularity = {}

    for a_log in log:

        # if id is already in popularity dictionary
        if a_log[1] in books_by_popularity:
            # increment value mapped to this id by one
            books_by_popularity[a_log[1]] += 1
        else:
            # generates new entry for novel id and sets value to 1
            books_by_popularity[a_log[1]] = 1

    # account for books not in log and set their count to 0
    for book in db:

        if book[0] not in books_by_popularity:
            books_by_popularity[book[0]] = 0

    return books_by_popularity


'''

The translate function takes in a list of book ids and returns a list of corresponding book titles 

'''


def translate(list_of_book_ids):

    output = ""

    book_titles = []

    for book_id in list_of_book_ids:

        for book in db:

            # make sure we don't repeat book titles to account for copies of the same book
            if book_id == book[0] and book[2] not in book_titles:
                book_titles.append(book[2])

    for title in book_titles:
        output = output+title+"\n"

    return output

# ---------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------------TESTING------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':

    # Test that update() creates local lists of the book entries and the logs
    print("1")
    print(db)
    print(log)

    print("\n")

    # Test that overdue() returns a boolean value for whether a book is overdue or not
    print("2a", overdue(['1', 'Romance', 'The Notebook', 'Nicolas Sparks', '1/8/2010', 'VSPW']))
    print("2b", overdue(['23', 'Historical', 'Emperor: The Gates of Rome', 'Conn Igulden', '19/12/2016', '0']))

    print("\n")

    # Test that available() returns a boolean value for whether a book is avaiable for checkout
    print("3a", available("1"))
    print("3b", available("23"), "\n")

    # Test that history returns the id of the member's last read book and all the books the member has read before
    print("4a", history("FAYE"))
    # Test that history returns empty lists for member's who have never read a book before
    print("4b", history("faye"), "\n")

    # Test that genre list returns a list of books that are of the same genre as the book argument,
    # duplicate values are insignificant
    print("5", genre_list("9"), "\n")

    # Test the most_popular_books() returns a dictionary with every book id as the key
    # and the checkout frequency as its value
    print("6", most_popular_books(), "\n")

    # Test that translate() returns a list of book titles when a list of book ids is passed through it
    print("7", translate(['45', '42', '32', '23']), "\n")

    # Test that when checkout is called with a member id and a book id... 
    # ... the database is updated with abcd next to book 20 entry
    # ... a log entry is generated with present date as the checkout date, 0 as return date,
    # and the member id is at the end of the entry
    # !!!!!!!!! (comment out the return test below to check return date is set to 0)!!!!!!!!!!!!
    print("7", checkout("FIRA", "38"), "\n")

    # Test that when book_return is called with a book id...
    # ... the book entry in database.txt for id 38 is edited, id "FIRA" is no longer present next to the entry 
    # ... the log entry for the book's initial checkout is edited and the return date is set to present date
    print("8", book_return("38"))

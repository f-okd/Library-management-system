import database
# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
'''

Bookrecommend.py module contains one function, recommend_book(member_id).
recommend_book function takes in a member id and validates that the input is of an acceptable format.
It retrieves the member's last read book and all the books they have read before, and how many times.
It also retrieves a list of the overall most popular books, aka best sellers. 
New members or members who haven't read a book before are recommended the top 10 most frequently checked out books. 
Otherwise it identifies the genre of the member's last read book and recommends up to 10 of the next most popular books
in that same genre. 
If the number of recommended books is less than 3 then the overall best selling books are then recommended.

'''


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


def recommend_book(member_id):
    # VALIDATING MEMBER ID
    if len(member_id) == 4:
        if not member_id.isalpha():
            return "ERROR: Member ID can only contain letters"
    else:
        return "ERROR: Member ID must be 4 characters long"

    # get user's last read book
    last_read_book, read_books = database.history(member_id)

    # return dictionary of book ids (key) and frequency of checkout (value)
    books_by_popularity = database.most_popular_books()

    # return sorted list of tuples of all books and how much they have been withdrawn
    books_by_popularity = sorted((count, key) for key, count in books_by_popularity.items())

    # get id for the last 10 elements(the last elements will be the most withdrawn as it's sorted in ascending order)
    best_sellers = [id for _, id in books_by_popularity[-10:]]

    # if user has not read any books before or if they have read every book,
    # returns list of ids of the most popular books overall, regardless of genre
    if last_read_book == [] or len(read_books) == len(database.db):
        best_sellers = database.translate(best_sellers)
        return best_sellers

    # get the id of the last read book
    last_read_book = last_read_book[0]

    # get list of all books of same genre
    books_of_same_genre = database.genre_list(last_read_book)

    # return list of tuples of books of the same genre as the last book user read, and how much they've been withdrawn
    books_by_popularity = [(count, key) for count, key in books_by_popularity
                           if key in books_of_same_genre]

    # sort the list of books of the same genre as his last read book by popularity.
    books_by_popularity = sorted(books_by_popularity)

    # collect the ids of the most popular books of the same genre as the user's last read book
    recommended_books = [id for _, id in books_by_popularity if id not in read_books]

    # find the bestseller's that the user hasn't read,
    # this prevents duplicates from popping up when merging recommended_books with best_sellers
    unread_bestsellers = []
    for book in best_sellers:
        if book not in recommended_books:
            unread_bestsellers.append(book)

    # if there isn't at least 3 recommended books,
    # merge the recommended_books list with a list of bestseller's that the user hasn't read before
    if len(recommended_books) < 3:
        length = len(recommended_books)
        n = 10-length
        # recommend bestsellers after books they haven't read from same genre
        recommended_books += unread_bestsellers[-n:]

    # convert list of book ids into actual books
    recommended_books = database.translate(recommended_books)

    return recommended_books


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#



if __name__ == '__main__':
    
    #1
    # Validates that member ID can only contain letters
    print("1",recommend_book("1234"))

    # 2
    # Validates that Member ID can only be 4 characters long
 
    print("2",recommend_book("abcde"))


#FUNCTIONALITY TESTING
    # 3
    # User QWER has no log entries
    # Should recommend list of best sellers
    print("3",recommend_book("QWER"))

    # 4
    # User FAYE's last read book (at the time of writing this) was Emperor: The Gates of Rome, a historical book
    # Should recommend list of historical books
    print("4",recommend_book("FAYE"))


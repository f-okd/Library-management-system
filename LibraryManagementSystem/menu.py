# import tkinter module to produce gui
from tkinter import *
from tkinter import ttk

import bookrecommend
import booksearch
import bookcheckout
import bookreturn


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#

"""
The structure of this menu was to have every page defined in a function and as a frame. 
Calling a page's function should destroy what is on the root window, and instantiate a new frame with new widgets.

home_page contains 4 buttons which take you to all the other pages. When the function is called it clears whatever is on
the window and generates the buttons again, so if this function is called while another frame is active then that frame 
is cleared.
"""


def home_page(root):
    root.winfo_children()[0].destroy()

    home_frame = Frame(root, height="800", width="600")

    welcome_message = Label(home_frame, text="Welcome to the Library service!", font=("Times", 23), justify="center")
    
    search_button = Button(home_frame, text="Look Up Book", font=("Times", 23), bd=10,
                           command=lambda: book_search(root))

    checkout_button = Button(home_frame, text="Checkout a book",
                             font=("Times", 23), bd=10, command=lambda: book_checkout(root))

    return_button = Button(home_frame, text="Return a book", font=("Times", 23), bd=10,
                           command=lambda: book_return(root))

    recommend_button = Button(home_frame, text="Get a book recommendation", font=("Times", 23), bd=10,
                              command=lambda: book_recommend(root))

    buttons = (welcome_message, search_button, checkout_button, return_button, recommend_button)

    for i, widget in enumerate(buttons):
        widget.pack()
        widget.place(x=0, y=100*i, width=600, height=100)
    
    home_frame.pack()


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
output_result is used solely for the book search function, it takes a list of books and their attributes and places them
in a tree.
"""


def output_result(tree, books):
    # we want to clear the tree every time a new search is made
    for child in tree.get_children():
        tree.delete(child)
    
    for book, status in books:
        tag = "not overdue"
        if status:
            tag = "ovr"
        tree.insert('', 0, values=book, tag=tag)

    tree.tag_configure("ovr", foreground="red", font=("", 10, "bold"))


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
book_search function clears the previous frame on the window and creates a new frame including all widgets required for 
book_search. 

It has an entry box for the user to enter a book title to search for, if the book exists in the database 
then it is displayed in the treeview below the entry box, including all its attributes.

Below the treeview is a button that when pressed takes you back to the homepage by calling home_page().
"""


def book_search(root):
    # winfo_children() returns list of all widgets on a window,
    # we know there is only one frame in homepage, so we use index 0.
    root.winfo_children()[0].destroy()

    search_frame = Frame(root, height="800", width="600")

    message = Label(search_frame, text="Enter the name of the book you are looking for", font=("Times", 23),
                    justify="center")

    book_entry = Entry(search_frame, font=("", 18))

    # make it so that the book will automatically be shown in tree view without the user having to press a button
    book_entry.bind("<KeyRelease>", lambda _: output_result(tree, booksearch.search_title(book_entry.get())))

    columns = ("ID", "Genre", "Title", "Author", "Date Purchased", "On loan to")

    sizes = ("50", "50", "150", "100", "70", "50",)

    tree = ttk.Treeview(search_frame, columns=columns, show='headings')

    for column, size in zip(columns, sizes):
        tree.column(column, width=size)
        tree.heading(column, text=column)

    homepage_button = Button(search_frame, text="Main menu", font=("Times", 15), bd=5, command=lambda: home_page(root))

    widgets = ((message, 0, 100, 600), (book_entry, 0, 100, 600), (tree, 0, 100, 600), (homepage_button, 150, 50, 300))

    i = 0

    for widget, x, height, width in widgets:
        widget.pack()
        widget.place(x=x, y=100*i, width=width, height=height)  
        i += 1

    search_frame.pack()

# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#

"""
print_result is used to display a text label on any frame, by taking a string and frame argument
"""


def print_result(frame, sentence):

    sentence_label = Label(frame, text=sentence, font=("Times", 15))

    sentence_label.pack()

    # defined width and height so that labels on the same frame completely overlap, sometimes a new shorter output...
    # ...will still show the previous message behind it
    sentence_label.place(x=0, y=250, width=600, height=50)


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
book_checkout clears whatever frame was previously on the window. 

It then creates a new frame and on this frame is two entries next to each entry is a label prompting the user to enter a
member ID and a book ID. 

Below this is a checkout button upon pressing the button the withdraw() function from bookcheckout.py is called using 
the retrieved values from the two entries.

The output is displayed on the frame using print_result()

Below the checkout button is a button that when pressed takes you back to the homepage by calling home_page()
"""


def book_checkout(root):
    root.winfo_children()[0].destroy()

    checkout_frame = Frame(root, height="800", width="600")

    enter_member_label = Label(checkout_frame, text="Enter member ID", font=("Times", 20))

    enter_book_label = Label(checkout_frame, text="Enter book ID", font=("Times", 20))

    member_id_entry = Entry(checkout_frame, font=("Times", 18))

    book_id_entry = Entry(checkout_frame, font=("Times", 18))

    withdraw_button = Button(checkout_frame, text="Withdraw", font=("Times", 15), command=lambda:
                             print_result(checkout_frame, bookcheckout.withdraw(member_id_entry.get(),
                                                                                book_id_entry.get())))

    homepage_button = Button(checkout_frame, text="Main menu", font=("Times", 15), bd=5,
                             command=lambda: home_page(root))

    widgets = [enter_member_label, enter_book_label, member_id_entry, book_id_entry, withdraw_button, homepage_button]

    for widget in widgets:
        widget.pack()

    enter_member_label.place(x=0, y=15)
    member_id_entry.place(x=200, y=10, width=300, height=50)

    enter_book_label.place(x=0, y=125)
    book_id_entry.place(x=200, y=120, width=300, height=50)

    withdraw_button.place(x=250, y=200, width=100, height=30)
    homepage_button.place(x=150, y=400, width=300, height=50)
    checkout_frame.pack()


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
book_return clears whatever frame was previously on the window. 

It then creates a new frame and on this frame is an entry with a label next to it prompting the user to enter the id of
the book they want to return.

Below this is a return button that when pressed calls the return_book() function from bookreturn.py using the value
retrieved from the book id entry.

Below the return button is a button that when pressed takes you back to the homepage by calling home_page()
"""


def book_return(root):
    # clear window
    root.winfo_children()[0].destroy()

    return_frame = Frame(root, height="800", width="600")

    return_book_label = Label(return_frame, text="Enter book ID", font=("Times", 20))

    return_book_entry = Entry(return_frame, font=("Times", 18))

    return_book_button = Button(return_frame, text="Return", font=("Times", 15), command=lambda:
                                print_result(return_frame, bookreturn.return_book(return_book_entry.get())))

    homepage_button = Button(return_frame, text="Main menu", font=("Times", 15), bd=5, command=lambda: home_page(root))

    widgets = [return_frame, return_book_label, return_book_entry, homepage_button, return_book_button]

    for widget in widgets:
        widget.pack()

    return_book_label.place(x=40, y=10)

    return_book_entry.place(x=250, y=10)

    return_book_button.place(x=250, y=100, width=100, height=30)

    homepage_button.place(x=150, y=400, width=300, height=50)


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
print_result2 is similar to the other print result except it also specifies the height alongside the width, 
as multiple lines are printed this time, if height is not specified, a shorter output may overlap the previous output, 
and the previous output will still be visible, which is problematic.

This part is only relevant to the book_recommend function and will alter the layout of other the frames negatively 
"""


def print_result2(frame, sentence):
    # we want to clear the tree every time a new search is made
    sentence_label = Label(frame, text=sentence, font=("Times", 15))

    sentence_label.pack()

    sentence_label.place(x=0, y=150, width=600, height=350)


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
book_recommend clears whatever frame was previously on the window.
 
It then creates a new frame and on this frame is an entry with a label next to it prompting the user to enter the id of
member looking for a book recommendation.

There is a recommend button below this that when pressed calls recommend_book() from bookrecommend.py using the value
retrieved from the member id entry.

There is a homepage button at the bottom that when pressed calls home_page() and takes you back to the main menu/hompage
"""


def book_recommend(root):
    # clear window
    root.winfo_children()[0].destroy()

    recommend_frame = Frame(root, height="800", width="600")

    recommend_label = Label(recommend_frame, text="Enter member ID", font=("Times", 20))

    recommend_entry = Entry(recommend_frame, font=("Times", 18))

    recommend_book_button = Button(recommend_frame, text="Recommend", font=("Times", 15), command=lambda:
                                   print_result2(recommend_frame, bookrecommend.recommend_book(recommend_entry.get())))

    homepage_button = Button(recommend_frame, text="Main menu", font=("Times", 15), bd=5, command=lambda:
                             home_page(root))

    widgets = [recommend_frame, recommend_entry, recommend_label, recommend_book_button]

    for widget in widgets:
        widget.pack()

    recommend_label.place(x=40, y=10)

    recommend_entry.place(x=250, y=10)

    recommend_book_button.place(x=250, y=100, width=110, height=30)

    homepage_button.place(x=150, y=500, width=300, height=50)


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


"""
main() creates a blank window then calls the home_page() function to bring up the homepage
"""


def main():

    root = Tk()

    root.geometry("800x600")

    # blank frame so that when I destroy the children of root at the start of homepage() no index error is returned

    start_frame = Frame(root, height="800", width="600")

    start_frame.pack()

    home_page(root)

    root.mainloop()


# ----------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


main()

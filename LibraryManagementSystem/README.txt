Some init tests are commented out at the bottom of a few modules.
This is because the tests change the status of books and edit the log/database before you can record their initial state and cotnrast with after the test is run.
But they can be removed from the comments at your discretion, it doesn't affect whether not the code works.
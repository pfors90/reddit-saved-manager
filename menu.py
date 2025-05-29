import pyinputplus as pyip

import CustomExceptions
import utilities

MENU_ITEMS = 3

def print_menu():
    print("***** REDDIT SAVED MANAGER *****")
    print("Please choose from the following options:")
    print("1. Full saved post import")
    print("2. Partial / recent saved post import")
    print("3. Exit")

def parse_menu_option(app, option):
    if option == 1:
        print("Perform a full import of all your saved posts?")
        print("This may take some time!")
        confirm = pyip.inputYesNo("Y/N: ")

        if confirm == "no":
            raise CustomExceptions.UserCancelledException("Full import of saved posts has been cancelled.")

        saved_items_praw = app.reddit.retrieve_saved(limit = None)

        saved_comments, saved_submissions = utilities.parse_posts(app, saved_items_praw)
        app.db.insert_comments(saved_comments)
        app.db.insert_submissions(saved_submissions)

    elif option == 2:
        print("Import up to 500 recent posts")
        limit = pyip.inputNum("Number to import: ", min = 1, max = 500)
        saved_items_praw = app.reddit.retrieve_saved(limit = limit)

        saved_comments, saved_submissions = utilities.parse_posts(app, saved_items_praw)
        app.db.insert_comments(saved_comments)
        app.db.insert_submissions(saved_submissions)

    else:
        raise CustomExceptions.InvalidMenuOptionException(f"Invalid menu option [{option}] entered.\nYou shouldn\'t have been able to do that\n")

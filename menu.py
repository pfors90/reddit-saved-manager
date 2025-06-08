import pyinputplus as pyip
from datetime import datetime

import CustomExceptions
import utilities

MENU_ITEMS = 5

def print_menu():
    print("***** REDDIT SAVED MANAGER *****")
    print("Please choose from the following options:")
    print("1. Full saved post import")
    print("2. Partial / recent saved post import")
    print("3. View database statistics")
    print("4. View comments by criteria")
    print("5. Exit")

def parse_menu_option(app, option):
    if option == 1:
        print("Perform a full import of all your saved posts?")
        print("This may take some time!")
        confirm = pyip.inputYesNo("Y/N: ")

        if confirm == "no":
            raise CustomExceptions.UserCancelledException("Full import of saved posts has been cancelled.")

        saved_items_praw = app.reddit.retrieve_saved(limit = None)

        saved_posts = utilities.parse_posts(app, saved_items_praw)
        app.db.insert_posts(saved_posts)

    elif option == 2:
        print("Import up to 500 recent posts")
        limit = pyip.inputNum("Number to import: ", min = 1, max = 500)
        saved_items_praw = app.reddit.retrieve_saved(limit = limit)

        saved_posts = utilities.parse_posts(app, saved_items_praw)
        app.db.insert_posts(saved_posts)

    elif option == 3:
        result_total = app.db.select_query(f"SELECT COUNT(*) FROM saved_posts")
        result_submission_total = app.db.select_query(f"SELECT COUNT(*) FROM saved_posts WHERE type=\"t3\"")
        result_comment_total = app.db.select_query("SELECT COUNT(*) FROM saved_posts WHERE type=\"t1\"")
        print(f"Total saved posts: {result_total[0][0]}")
        print(f"Total saved submissions: {result_submission_total[0][0]}")
        print(f"Total saved comments: {result_comment_total[0][0]}")
        print(f"View breakdown of posts by subreddit?")

        confirm = pyip.inputYesNo("Y/N: ")

        # TODO -----
        #  can this be paginated as well?
        if confirm == "yes":
            result_sub_breakdown = app.db.select_query(f"SELECT DISTINCT subreddit, COUNT(subreddit) FROM saved_posts GROUP BY subreddit ORDER BY lower(subreddit) ASC")
            for line in result_sub_breakdown:
                print(f"{line[0]}: {line[1]}")

        else:
            print("Returning to main menu...")

    elif option == 4:
        choice = input("View posts by: [D]ate range / [S]ubreddit: ").strip().lower()
        if choice == "d":
            start_date = pyip.inputDate("Start date [YYYY-MM-DD]: ", formats = ["%Y-%m-%d"], default = datetime.today().date())
            end_date = pyip.inputDate("End date [YYYY-MM-DD]: ", formats = ["%Y-%m-%d"], default = datetime.today().date())
            query = f"SELECT * FROM saved_posts WHERE date(created_time) BETWEEN '{start_date}' and '{end_date}'"

        elif choice == "s":
            subreddit = input("Enter subreddit: /r/").strip().lower()
            query = f"SELECT * FROM saved_posts WHERE subreddit LIKE '{subreddit}'"

        else: print("Invalid input, returning to main menu...")

        results = app.db.select_query(query)
        savedPosts = utilities.generate_objects_from_sql(results)

        utilities.paginate_posts(savedPosts)

        return

    else:
        raise CustomExceptions.InvalidMenuOptionException(f"Invalid menu option [{option}] entered.\nYou shouldn\'t have been able to do that\n")

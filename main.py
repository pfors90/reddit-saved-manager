import pyinputplus as pyip

from AppContext import AppContext
import menu

if __name__ == "__main__":
    app = AppContext("config.ini")
    app.db.create_tables()

    menu.print_menu()
    option = pyip.inputNum("Selection: ", min=1, max=menu.MENU_ITEMS)

    # final menu option will always be "Exit"
    while option != menu.MENU_ITEMS:
        # menu loop
        try:
            menu.parse_menu_option(app, option)
        except Exception as e:
            print(f"Operation cancelled\nError: {e}\n")
            # ?? - traceback.print_exc()

        menu.print_menu()
        option = pyip.inputNum("Selection: ", min=1, max=menu.MENU_ITEMS)

    # make sure to close the DB cursor and connection on exit
    app.db.close()
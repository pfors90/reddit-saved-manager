from AppContext import AppContext

if __name__ == "__main__":
    app = AppContext('config.ini')

    app.db.create_tables()

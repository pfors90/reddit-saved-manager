import database as db

# temporary until config file is implemented
db_file = "Y:\\Code\\reddit-saved-manager\\database.sqlite"

if __name__ == "__main__":
    connection = db.create_connection(db_file)

    createSavedTable = """
        CREATE TABLE IF NOT EXISTS saved_posts (
            post_id PRIMARY KEY,
            subreddit VARCHAR(50),
            post_type VARCHAR(10),
            title VARCHAR(100),
            author VARCHAR(100),
            link VARCHAR(150),
            body TEXT,
            upvotes INTEGER,
            popularity INTEGER,
            NSFW BOOLEAN
        );
        """

    db.execute_query(connection, createSavedTable)
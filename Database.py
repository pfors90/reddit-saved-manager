import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = None
        print(f'Connecting to {db_file}')
        try:
            self.connection = sqlite3.connect(db_file)
            self.cursor = self.connection.cursor()
            print(f'Connection to database file at "{db_file}" successful')
        except sqlite3.Error as e:
            print(f'Error: {e}')

    def create_tables(self):
        create_saved_comment_table = """
                CREATE TABLE IF NOT EXISTS saved_comments (
                    id VARCHAR(12) PRIMARY KEY,
                    author VARCHAR(100),
                    body TEXT,
                    body_html TEXT,
                    created_time TIMESTAMP,
                    link_id VARCHAR(12),
                    permalink VARCHAR(300),
                    score INTEGER,
                    post_title VARCHAR(250),
                    subreddit VARCHAR(50)
                );
                """

        create_saved_submission_table = """
                CREATE TABLE IF NOT EXISTS saved_submissions (
                    id VARCHAR(12) PRIMARY KEY,
                    author VARCHAR(100),
                    created_time TIMESTAMP,
                    NSFW BOOLEAN,
                    permalink VARCHAR(300),
                    score INTEGER,
                    subreddit VARCHAR(50),
                    title VARCHAR(250),
                    upvote_ratio INTEGER,
                    url VARCHAR(500)
                );
                """

        self.execute_query(create_saved_comment_table)
        self.execute_query(create_saved_submission_table)

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print('Query executed successfully')
        except sqlite3.Error as e:
           print(f'Error: {e}')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
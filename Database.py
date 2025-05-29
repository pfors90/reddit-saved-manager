import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = None
        print(f"Connecting to \"{db_file}\"")
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            print(f"Connection to database file at \"{db_file}\" successful")
        except sqlite3.Error as e:
            print(f"Error: {e}")

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
                    post_title_retrieved BOOLEAN,
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
            self.conn.commit()
            print("Query executed successfully")
        except sqlite3.Error as e:
            print(f"Error [{e}] when executing query:")
            print(query)

    def insert_comments(self, comments):
        # the following ~11 lines are duplicated in this method and insert_submissions()
        # should it be moved to a get_existing_ids(self, type) method?
        # used to ensure that we don't attempt to insert an existing submission ID into the database
        if not comments:
            return

        insert_comment_ids = [c.id for c in comments]
        placeholder = ",".join(["?"] * len(insert_comment_ids))
        query = f"SELECT id FROM comments WHERE id IN ({placeholder})"

        cursor = self.conn.execute(query, insert_comment_ids)
        existing_ids = {row[0] for row in cursor.fetchall()}

        new_comments = [c for c in comments if c.id not in existing_ids]

        # TODO -----
        #  setup a try/except block here to handle issues with the query not executing properly
        # setup and execute the query
        values = [(c.id, c.author, c.body, c.body_html, c.created_time, c.link_id, c.permalink, c.score, c.subreddit, c.post_title_retrieved, c.post_title) for c in new_comments]
        self.conn.executemany("""
            INSERT INTO comments (id, author, body, body_html, created_time, link_id, permalink, score, subreddit, post_title_retrieved, post_title)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)
        """, values)
        self.conn.commit()

    def insert_submissions(self, submissions):
        # the following ~11 lines are duplicated in this method and insert_comments()
        # should it be moved to a get_existing_ids(self, type) method?
        # used to ensure that we don't attempt to insert an existing submission ID into the database
        if not submissions:
            return

        insert_submission_ids = [s.id for s in submissions]
        placeholder = ",".join(["?"] * len(insert_submission_ids))
        query = f"SELECT id FROM submissions WHERE id IN ({placeholder})"

        cursor = self.conn.execute(query, insert_submission_ids)
        existing_ids = {row[0] for row in cursor.fetchall()}

        new_submissions = [s for s in submissions if s.id not in existing_ids]

        # TODO -----
        #  setup a try/except block here to handle issues with the query not executing properly
        # setup and execute the query
        values = [(s.id, s.author, s.created_time, s.NSFW, s.permalink, s.score, s.subreddit, s.title, s.upvote_ratio, s.url) for s in new_submissions]
        self.conn.executemany("""
            INSERT INTO submissions (id, author, created_time, NSFW, permalink, score, subreddit, title, upvote_ratio, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)

        self.conn.commit()

    # TODO -----
    #  is there a way to automatically invoke this method when the object is destroyed?
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
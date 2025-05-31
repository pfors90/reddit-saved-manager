import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def create_tables(self):
        create_saved_posts_table = """
            CREATE TABLE IF NOT EXISTS saved_posts (
                id VARCHAR(12) PRIMARY KEY,
                type VARCHAR(2),
                author VARCHAR(100),
                body TEXT,
                created_time TIMESTAMP,
                link_id VARCHAR(12),
                permalink VARCHAR(300),
                score INTEGER,
                subreddit VARCHAR(50),
                NSFW BOOLEAN,
                post_title TEXT,
                post_title_retrieved BOOLEAN,
                url TEXT,
                upvote_ratio FLOAT
            );
        """

        self.execute_query(create_saved_posts_table)

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error [{e}] when executing query:")
            print(query)

    def insert_posts(self, posts):
        if not posts:
            return

        insert_post_ids = [p.id for p in posts]
        placeholder = ",".join(["?"] * len(insert_post_ids))
        query = f"SELECT id FROM saved_posts WHERE id IN ({placeholder})"

        cursor = self.conn.execute(query, insert_post_ids)
        existing_ids = {row[0] for row in cursor.fetchall()}

        new_posts = [p for p in posts if p.id not in existing_ids]

        # TODO -----
        #  setup a try/except block here to handle issues with the query not executing properly
        # setup and execute the query
        values = [(
            p.id,
            p.type,
            p.author,
            p.body,
            p.created_time,
            p.link_id,
            p.permalink,
            p.score,
            p.subreddit,
            p.NSFW,
            p.title,
            p.post_title_retrieved,
            p.url,
            p.upvote_ratio
        ) for p in new_posts]

        self.conn.executemany("""
            INSERT INTO saved_posts (
                id,
                type,
                author,
                body,
                created_time,
                link_id,
                permalink,
                score,
                subreddit,
                NSFW,
                post_title,
                post_title_retrieved,
                url,
                upvote_ratio
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?)
        """, values)
        self.conn.commit()

    # TODO -----
    #  is there a way to automatically invoke this method when the object is destroyed?
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
from AppContext import AppContext
import RedditHandler as api

if __name__ == "__main__":
    app = AppContext('config.ini')

    createSavedCommentTable = """
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

    createSavedSubmissionTable = """
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

    app.db.execute_query(app, createSavedCommentTable)
    app.db.execute_query(app, createSavedSubmissionTable)

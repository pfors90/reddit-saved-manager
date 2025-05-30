from datetime import datetime
import os

from Database import Database
from SavedPost import SavedPost

def test_create_tables():
    test_db_path = "test_database.sqlite"
    db = Database(test_db_path)
    db.create_tables()

    # query the database to get the names of all existing tables
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in db.cursor.fetchall()}

    # assert that the appropriate tables exist in our database
    assert "saved_posts" in tables

    # wipe the temporary database for fresh future testing
    db.close()
    os.remove(test_db_path)

def test_insert_posts():
    test_db_path = "test_database.sqlite"
    db = Database(test_db_path)
    db.create_tables()

    # create sample SavedPost objects to write to the database
    test_comment_1 = SavedPost(
        id = "t1_abc123",
        type = "t1",
        author = "test_author",
        body = "test body",
        created_time = datetime.now(),
        link_id = "t3_def456",
        permalink = "/testsub/t3_def456/t1_abc123",
        score = 42,
        subreddit = "testsub",
        NSFW = False,
        title = "Test Post 1",
        post_title_retrieved = True,
        url = "https://www.google.com/",
        upvote_ratio = 0.00
    )

    test_submission_1 = SavedPost(
        id = "t3_ghi789",
        type = "t3",
        author = "test_author_2",
        body = "",
        created_time = datetime.now(),
        link_id = "t3_ghi789",
        permalink = "/testsub/t3_ghi798",
        score = 64,
        subreddit = "testsub2",
        NSFW = True,
        title = "Test Post 2",
        post_title_retrieved = True,
        url = "https://www.reddit.com/",
        upvote_ratio = 0.70
    )

    posts = [test_comment_1, test_submission_1]

    # insert the comments
    db.insert_posts(posts)

    db.cursor.execute("SELECT * FROM saved_posts WHERE id IN (?, ?)", ("t1_abc123", "t3_ghi789"))
    result = db.cursor.fetchall()

    # assert that we got 2 records back
    assert len(result) == 2

    # wipe the temporary database for fresh future testing
    db.close()
    os.remove(test_db_path)
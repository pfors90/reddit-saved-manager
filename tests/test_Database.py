from datetime import datetime
import os

from Database import Database
from SavedPost import SavedComment, SavedSubmission

def test_create_tables():
    test_db_path = "test_database.sqlite"
    db = Database(test_db_path)
    db.create_tables()

    # query the database to get the names of all existing tables
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in db.cursor.fetchall()}

    # assert that the appropriate tables exist in our database
    assert "saved_comments" in tables
    assert "saved_submissions" in tables

    # wipe the temporary database for fresh future testing
    db.close()
    os.remove(test_db_path)

def test_insert_comments():
    test_db_path = "test_database.sqlite"
    db = Database(test_db_path)
    db.create_tables()

    # create sample SavedComment objects to write to the database
    test_comment_1 = SavedComment(
        id = "abc123",
        author = "testuser",
        created_time = datetime.now(),
        permalink = "/r/testing/comments/abc123",
        score = 42,
        subreddit = "testing",
        body = "Test comment",
        body_html = "<b>Test comment</b>",
        link_id = "t3_xyz",
    )
    test_comment_1.post_title_retrieved = True
    test_comment_1.post_title = "Test Post 1"

    test_comment_2 = SavedComment(
        id = "def456",
        author = "testuser2",
        created_time = datetime.now(),
        permalink = "/r/testing2/comments/def456",
        score = 42,
        subreddit = "testing2",
        body = "Test comment 2",
        body_html = "<i>Test comment 2</i>",
        link_id = "t3_def456",
    )
    test_comment_2.post_title_retrieved = True
    test_comment_2.post_title = "Test Post 2"

    comments = [test_comment_1, test_comment_2]

    # insert the comments
    db.insert_comments(comments)

    db.cursor.execute("SELECT * FROM saved_comments WHERE id IN (?, ?)", ("abc123", "def456"))
    result = db.cursor.fetchall()

    # assert that we got 2 records back
    assert len(result) == 2

    # wipe the temporary database for fresh future testing
    db.close()
    os.remove(test_db_path)


def test_insert_submissions():
    test_db_path = "test_database.sqlite"
    db = Database(test_db_path)
    db.create_tables()

    # create sample SavedSubmission objects to write to the database
    test_submission_1 = SavedSubmission(
        id="abc123",
        author="testuser",
        created_time=datetime.now(),
        permalink="/r/python/comments/abc123/",
        score=100,
        subreddit="python",
        NSFW=False,
        title="First test submission",
        upvote_ratio=0.95,
        url="https://www.wikipedia.org/"
    )

    test_submission_2 = SavedSubmission(
        id="def456",
        author="testuser2",
        created_time=datetime.now(),
        permalink="/r/coding/comments/def456/",
        score=150,
        subreddit="coding",
        NSFW=True,
        title="Second test submission (NSFW)",
        upvote_ratio=0.87,
        url="https://www.reddit.com/r/coding/comments/def456/"
    )

    submissions = [test_submission_1, test_submission_2]

    # insert the comments
    db.insert_submissions(submissions)

    db.cursor.execute("SELECT * FROM saved_submissions WHERE id IN (?, ?)", ("abc123", "def456"))
    result = db.cursor.fetchall()

    # assert that we got 2 records back
    assert len(result) == 2

    # wipe the temporary database for fresh future testing
    db.close()
    os.remove(test_db_path)
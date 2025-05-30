from datetime import datetime
from SavedPost import SavedPost

def test_saved_comment_str_output():
    comment = SavedPost(
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

    result = str(comment)
    assert "Test Post 1" in result, "\'Test Post 1\' not found in output"
    assert "[testsub]" in result, "\'[testsub]\' not found in output"

def test_saved_submission_str_output():
    submission = SavedPost(
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

    result = str(submission)
    assert "Test Post 2" in result, "\'Test Post 2\' not found in output"
    assert "test_author_2" in result, "\'test_author_2\' not found in output"
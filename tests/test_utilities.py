from unittest.mock import patch, MagicMock

import utilities

# parse POST - singular
def test_parse_post_comment():
    mock_praw_comment_1 = MagicMock()
    mock_praw_comment_1.fullname = "t1_abc123"
    mock_praw_comment_1.author = "test_author_1"
    mock_praw_comment_1.body_html = "<em>test body</em>"
    mock_praw_comment_1.created_utc = 1700000000
    mock_praw_comment_1.link_id = "t3_retrieve_1"
    mock_praw_comment_1.permalink = "/testsub1/t1_abc123"
    mock_praw_comment_1.score = 64
    mock_praw_comment_1.subreddit = "testsub1"

    saved_comment = utilities.parse_post(mock_praw_comment_1)

    assert isinstance(saved_comment, utilities.SavedPost)
    assert saved_comment.type == "t1"
    assert saved_comment.title == "[Unknown]"
    assert saved_comment.post_title_retrieved == False


def test_parse_post_submission():
    mock_praw_submission_1 = MagicMock()
    mock_praw_submission_1.fullname = "t3_abc123"
    mock_praw_submission_1.author = "test_author_3"
    mock_praw_submission_1.created_utc = 1700000002
    mock_praw_submission_1.over_18 = False
    mock_praw_submission_1.permalink = "/testsub3/t3_abc123"
    mock_praw_submission_1.score = 87
    mock_praw_submission_1.subreddit = "testsub3"
    mock_praw_submission_1.title = "Mock Submission Title 1"
    mock_praw_submission_1.upvote_ratio = 0.50
    mock_praw_submission_1.url = "https://www.google.com/"
    mock_praw_submission_1.selftext = "Self text test 1"
    mock_praw_submission_1.body = None # have to define body for proper test due to the way MagicMock works

    saved_submission = utilities.parse_post(mock_praw_submission_1)

    assert isinstance(saved_submission, utilities.SavedPost)
    assert saved_submission.type == "t3"
    assert saved_submission.score == 87
    assert saved_submission.post_title_retrieved == True
    assert saved_submission.body == "Self text test 1"

# parse POSTS - plural
def test_parse_posts():
    # create mock AppContext because utilities.parse_posts needs an AppContext argument
    mock_app = MagicMock()
    mock_app.reddit = MagicMock()

    # create mock comments and submissions for parsing
    mock_praw_comment_1 = MagicMock()
    mock_praw_comment_1.fullname = "t1_abc123"
    mock_praw_comment_1.author = "test_author_1"
    mock_praw_comment_1.body_html = "<em>test body</em>"
    mock_praw_comment_1.created_utc = 1700000000
    mock_praw_comment_1.link_id = "t3_retrieve_1"
    mock_praw_comment_1.permalink = "/testsub1/t1_abc123"
    mock_praw_comment_1.score = 64
    mock_praw_comment_1.subreddit = "testsub1"

    mock_praw_comment_2 = MagicMock()
    mock_praw_comment_2.fullname = "t1_def456"
    mock_praw_comment_2.author = "test_author_2"
    mock_praw_comment_2.body_html = "<em>just testing</em>"
    mock_praw_comment_2.created_utc = 1700000001
    mock_praw_comment_2.link_id = "t3_retrieve_2"
    mock_praw_comment_2.permalink = "/testsub2/t1_def456"
    mock_praw_comment_2.score = 61
    mock_praw_comment_2.subreddit = "testsub2"

    mock_praw_submission_1 = MagicMock()
    mock_praw_submission_1.fullname = "t3_abc123"
    mock_praw_submission_1.author = "test_author_3"
    mock_praw_submission_1.created_utc = 1700000002
    mock_praw_submission_1.over_18 = False
    mock_praw_submission_1.permalink = "/testsub3/t3_abc123"
    mock_praw_submission_1.score = 87
    mock_praw_submission_1.subreddit =  "testsub3"
    mock_praw_submission_1.title = "Mock Submission Title 1"
    mock_praw_submission_1.upvote_ratio = 0.50
    mock_praw_submission_1.url =  "https://www.google.com/"
    mock_praw_submission_1.selftext = "Self text test 1"
    mock_praw_submission_1.body = None  # have to define body for proper test due to the way MagicMock works

    mock_praw_submission_2 = MagicMock()
    mock_praw_submission_2.fullname = "t3_def456"
    mock_praw_submission_2.author = "test_author_4"
    mock_praw_submission_2.created_utc = 1700000003
    mock_praw_submission_2.over_18 = True
    mock_praw_submission_2.permalink = "/testsub4/t3_def456"
    mock_praw_submission_2.score = 90
    mock_praw_submission_2.subreddit = "testsub4"
    mock_praw_submission_2.title = "Mock Submission Title 2"
    mock_praw_submission_2.upvote_ratio = 0.42
    mock_praw_submission_2.url =  "https://www.wikipedia.org/"
    mock_praw_submission_2.selftext = ""
    mock_praw_submission_2.body = None  # have to define body for proper test due to the way MagicMock works

    praw_posts = [mock_praw_comment_1, mock_praw_submission_1, mock_praw_submission_2, mock_praw_comment_2]

    # create mock return values matching praw_comment link_ids for praw .info() call
    mock_return_submission_1 = MagicMock()
    mock_return_submission_1.fullname = "t3_retrieve_1"
    mock_return_submission_1.title = "Mock Lookup Title 1"
    mock_return_submission_2 = MagicMock()
    mock_return_submission_2.fullname = "t3_retrieve_2"
    mock_return_submission_2.title = "Mock Lookup Title 2"

    mock_app.reddit.get_submissions_by_ids.return_value = [mock_return_submission_1, mock_return_submission_2]

    saved_posts = utilities.parse_posts(mock_app, praw_posts)

    # validate that the proper values were used for lookup
    call_args = mock_app.reddit.get_submissions_by_ids.call_args[0][0]
    assert set(call_args) == set(["t3_retrieve_1", "t3_retrieve_2"])

    filled_titles = [p.post_title for p in saved_posts if p.type == "t1"]
    assert "Mock Lookup Title 1" in filled_titles
    assert "Mock Lookup Title 2" in filled_titles

    assert saved_posts[0].post_title_retrieved == True

    assert isinstance(saved_posts[0], utilities.SavedPost)
    assert isinstance(saved_posts[2], utilities.SavedPost)



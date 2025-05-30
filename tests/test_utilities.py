from unittest.mock import patch, MagicMock

import utilities

def test_parse_posts():
    # create mock AppContext because utilities.parse_posts needs an AppContext argument
    mock_app = MagicMock()
    mock_app.reddit = MagicMock()

    # create mock comments and submissions for parsing
    mock_praw_comment_1 = MagicMock()
    mock_praw_comment_1.fullname = "t1_abc123"
    mock_praw_comment_1.author = "test_author_1"
    mock_praw_comment_1.body = "test body"
    mock_praw_comment_1.body_html = "<em>test body</em>"
    mock_praw_comment_1.created_utc = 1700000000
    mock_praw_comment_1.link_id = "t3_retrieve_1"
    mock_praw_comment_1.permalink = "/testsub1/t1_abc123"
    mock_praw_comment_1.score = 64
    mock_praw_comment_1.subreddit = "testsub1"

    mock_praw_comment_2 = MagicMock()
    mock_praw_comment_2.fullname = "t1_def456"
    mock_praw_comment_2.author = "test_author_2"
    mock_praw_comment_2.body = "just testing"
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

    praw_posts = [mock_praw_comment_1, mock_praw_submission_1, mock_praw_submission_2, mock_praw_comment_2]

    # create mock return values matching praw_comment link_ids for praw .info() call
    mock_return_submission_1 = MagicMock()
    mock_return_submission_1.fullname = "t3_retrieve_1"
    mock_return_submission_1.title = "Mock Lookup Title 1"
    mock_return_submission_2 = MagicMock()
    mock_return_submission_2.fullname = "t3_retrieve_2"
    mock_return_submission_2.title = "Mock Lookup Title 2"

    mock_app.reddit.get_submissions_by_ids.return_value = [mock_return_submission_1, mock_return_submission_2]

    saved_comments, saved_submissions = utilities.parse_posts(mock_app, praw_posts)

    # validate that the proper values were used for lookup
    call_args = mock_app.reddit.get_submissions_by_ids.call_args[0][0]
    assert set(call_args) == set(["t3_retrieve_1", "t3_retrieve_2"])

    filled_titles = [c.post_title for c in saved_comments]
    assert "Mock Lookup Title 1" in filled_titles
    assert "Mock Lookup Title 2" in filled_titles

    assert saved_comments[0].post_title_retrieved == True

    assert isinstance(saved_comments[0], utilities.SavedComment)
    assert isinstance(saved_submissions[1], utilities.SavedSubmission)



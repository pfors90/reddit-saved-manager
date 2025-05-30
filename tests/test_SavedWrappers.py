def test_saved_comment_str_output():
    from datetime import datetime
    from SavedPost.comment import SavedComment

    comment = SavedComment(
        id="abc123",
        author="testuser",
        body="Test comment body",
        body_html="<p>Test comment body</p>",
        created_time=datetime(2025, 5, 27, 17, 24),
        link_id="t3_abcxyz",
        permalink="/r/test/comments/abc123",
        score=42,
        subreddit="testsub"
    )

    comment.post_title = "Interesting Post"
    comment.post_title_retrieved = True

    result = str(comment)
    assert "Interesting Post" in result, "\'Interesting Post\' not found in output"
    assert "[testsub]" in result, "\'[testsub]\' not found in output"

def test_saved_submission_str_output():
    from datetime import datetime
    from SavedPost.submission import SavedSubmission

    submission = SavedSubmission(
        id="abc123",
        author="testuser",
        created_time=datetime(2025, 5, 27, 17, 24),
        NSFW=False,
        permalink="t3_abcxyz",
        score=42,
        subreddit="testsub",
        title="Interesting Post",
        upvote_ratio=0.5,
        url="https://www.reddit.com/r/test/comments/abc123",
    )

    result = str(submission)
    assert "Interesting Post" in result, "\'Interesting Post\' not found in output"
    assert "testuser" in result, "\'testuser\' not found in output"
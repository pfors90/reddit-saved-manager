from unittest.mock import patch, MagicMock
from RedditHandler import RedditHandler

def test_authentication_sets_reddit_instance():
    # create mock config class with data needed to authenticate a reddit instance
    mock_config = MagicMock()
    mock_config.CLIENT_ID = "id"
    mock_config.CLIENT_SECRET = "secret"
    mock_config.PASSWORD = "pass"
    mock_config.USER_AGENT = "agent"
    mock_config.USERNAME = "user"

    # abstract out the actual reddit instance so we don't needlessly hit the API
    with patch("RedditHandler.praw.Reddit") as mock_reddit_class:
        mock_reddit_instance = MagicMock()
        mock_reddit_instance.user.me.return_value = "mockuser"
        mock_reddit_class.return_value = mock_reddit_instance

        # invoke the RedditHandler() constructor to get our mocked reddit instance
        reddit = RedditHandler(mock_config)

        # ensure that the constructor was only called once, and with the appropriate mocked config data
        mock_reddit_class.assert_called_once_with(
            client_id="id",
            client_secret="secret",
            password="pass",
            user_agent="agent",
            username="user",
        )

        # confirm that the instance returned by our constructor gives the appropriate .me() value
        assert reddit.reddit.user.me() == "mockuser"

def test_retrieve_saved_returns_saved_posts():
    # create mock config class with data needed to authenticate a reddit instance
    mock_config = MagicMock()
    mock_config.CLIENT_ID = "id"
    mock_config.CLIENT_SECRET = "secret"
    mock_config.PASSWORD = "pass"
    mock_config.USER_AGENT = "agent"
    mock_config.USERNAME = "user"

    # abstract out the actual reddit instance so we don't needlessly hit the API
    with patch("RedditHandler.praw.Reddit") as mock_reddit_class:
        mock_reddit_instance = MagicMock()
        mock_user = MagicMock()
        mock_user.saved.return_value = ["post1", "post2"]
        mock_user.me.return_value = mock_user

        mock_reddit_instance.user = mock_user
        mock_reddit_class.return_value = mock_reddit_instance

        # invoke the RedditHandler() constructor to get our mocked reddit instance
        reddit = RedditHandler(mock_config)
        # ensure .retrieve_saved() properly invoked .saved() on our reddit instance
        saved = reddit.retrieve_saved(limit=2)

        # assert that the mock saved posts were properly returned, and that .saved() was only called once
        assert saved == ["post1", "post2"]
        mock_user.saved.assert_called_once_with(limit=2)

def test_retrieve_saved_reauthenticates_on_error():
    # create mock config class with data needed to authenticate a reddit instance
    mock_config = MagicMock()
    mock_config.CLIENT_ID = "id"
    mock_config.CLIENT_SECRET = "secret"
    mock_config.PASSWORD = "pass"
    mock_config.USER_AGENT = "agent"
    mock_config.USERNAME = "user"

    # abstract out the actual reddit instance so we don't needlessly hit the API
    with patch("RedditHandler.praw.Reddit") as mock_reddit_class:
        working_instance = MagicMock()
        working_user = MagicMock()
        working_user.saved.return_value = ["post1"]
        working_user.me.return_value = working_user
        working_instance.user = working_user

        # create a broken instance to force re-auth
        broken_instance = MagicMock()
        broken_user = MagicMock()
        broken_user.saved.side_effect = Exception("Auth failed")
        broken_user.me.return_value = broken_user
        broken_instance.user = broken_user

        # sequence of reddit instances to be returned
        mock_reddit_class.side_effect = [broken_instance, working_instance]

        # invoke the RedditHandler() constructor to get our mocked reddit instance
        reddit = RedditHandler(mock_config)
        # ensure .retrieve_saved() properly invoked .saved() on our reddit instance
        saved = reddit.retrieve_saved(limit=1)

        # assert that the returned value equals our specified .saved() return value
        assert saved == ["post1"]

def test_get_submissions_by_ids_calls_info():
    # create mock config class with data needed to authenticate a reddit instance
    mock_config = MagicMock()
    mock_config.CLIENT_ID = "id"
    mock_config.CLIENT_SECRET = "secret"
    mock_config.PASSWORD = "pass"
    mock_config.USER_AGENT = "agent"
    mock_config.USERNAME = "user"

    # abstract out the actual reddit instance so we don't needlessly hit the API
    with patch("RedditHandler.praw.Reddit") as mock_reddit_class:
        mock_reddit_instance = MagicMock()
        mock_reddit_instance.info.return_value = ["sub1", "sub2"]
        mock_reddit_instance.user.me.return_value = "mockuser"
        mock_reddit_class.return_value = mock_reddit_instance

        # invoke RedditHandler constructor with a mock praw.Reddit object
        reddit = RedditHandler(mock_config)
        subs = reddit.get_submissions_by_ids(["t3_abc", "t3_def"])

        # ensure that .get_submissions_by_ids calls .info()
        mock_reddit_instance.info.assert_called_once_with(fullnames=["t3_abc", "t3_def"])
        assert subs == ["sub1", "sub2"]
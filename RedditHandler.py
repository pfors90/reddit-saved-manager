import praw
from typing import List

class RedditHandler:
    def __init__(self, config):
        self.config = config
        self.reddit = self._authenticate()

    # if 2FA flag is set in config.ini, then Config.py should prompt for 2FA code on auth
    def _authenticate(self):
        reddit = praw.Reddit(
            client_id = self.config.CLIENT_ID,
            client_secret = self.config.CLIENT_SECRET,
            password = self.config.PASSWORD,
            user_agent = self.config.USER_AGENT,
            username = self.config.USERNAME,
        )

        print("User authenticated as " + str(reddit.user.me()))

        return reddit

    def retrieve_saved(self, limit = 50):
        try:
            saved = self.reddit.user.me().saved(limit = limit)
            return list(saved)

        # theoretically, the only exception should be due to authentication
        # on Error, reauthenticate and then grab the saved posts
        except Exception as e:
            print(f"Session issue: {e}")
            print("Attempting reauthentication")
            self.reddit = self._authenticate()
            saved = self.reddit.user.me().saved(limit = limit)
            return list(saved)

    def get_submissions_by_ids(self, submission_ids: List[str]):
        submissions = self.reddit.info(fullnames = submission_ids)
        return list(submissions)
import praw

class RedditHandler:

    def __init__(self, config):
        self.config = config
        self.reddit = self._authenticate()

    def _authenticate(self):
        reddit = praw.Reddit(
            client_id = self.config.CLIENT_ID,
            client_secret = self.config.CLIENT_SECRET,
            password = self.config.PASSWORD,
            user_agent = self.config.USER_AGENT,
            username = self.config.USERNAME,
        )

        print("User authenticated as " + reddit.user.me())

        return reddit

    def retrieve_saved(self, limit = 50):
        try:
            saved = self.reddit.user.me().saved(limit = limit)
            return list(saved)

        except Exception as e:
            print("Session issue: {e}")
            print("Attempting reauthentication")
            self.reddit = self._authenticate()
            saved = self.reddit.user.me().saved(limit = limit)
            return list(saved)

    def get_submission_by_id(self, submission_ids):
        submissions = self.reddit.info(fullnames = submission_ids)
        return list(submissions)
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SavedPost:
    id: str
    type: str
    author: str
    body: str
    created_time: datetime
    link_id: str
    permalink: str
    score: int
    subreddit: str
    NSFW: bool = False
    post_title: str = "Unknown"
    post_title_retrieved: bool = False
    url: str = "Unknown"
    upvote_ratio: float = 0.00

    # TODO -----
    #  standardize this so that it looks better in pagination
    def __str__(self):
        if self.type == "t1":
            long_type = "Comment"
        elif self.type == "t3":
            long_type = "Submission"
        else:
            long_type = "Unknown"
        return(
            f"[{long_type}] -- /r/{self.subreddit} -- by {self.author} at {self.created_time} \n"
            f"Title: {self.post_title}\n"
            f"{self.body if self.body else '[no selftext]'}\n"
            f"https://old.reddit.com{self.permalink}")
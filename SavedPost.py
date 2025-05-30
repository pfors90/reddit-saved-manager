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
    title: str = "Unknown"
    post_title_retrieved: bool = False
    url: str = "Unknown"
    upvote_ratio: float = 0.00

    def __str__(self):
        if self.type == "t1":
            return(
                f"[{self.subreddit}] -- Post Title: {'not yet retrieved' if not self.post_title_retrieved else self.post_title}\n"
                f"{self.body}\n"
                f"Author: {self.author} -- {self.created_time} -- {self.permalink}"
            )
        elif self.type == "t3":
            return(
                f"{self.score} ({self.upvote_ratio}) -- [{self.subreddit}] -- \"{self.title}\"\n"
                f"Author: {self.author} -- {self.created_time} -- {self.url}"
            )
        else:
            return(f"Invalid post type [{self.type}]")
from dataclasses import dataclass

from .base import SavedPost

@dataclass
class SavedSubmission(SavedPost):
    NSFW: bool
    title: str
    upvote_ratio: float
    url: str

    def __str__(self):
        return (
            f"{self.score} ({self.upvote_ratio}) -- [{self.subreddit}] -- \"{self.title}\"\n"
            f"Author: {self.author} -- {self.created_time} -- {self.url}"
        )
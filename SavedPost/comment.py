from dataclasses import dataclass

from .base import SavedPost

@dataclass
class SavedComment(SavedPost):
    body: str
    body_html: str
    link_id: str
    post_title_retrieved = False # handles cases where title actually IS 'Unknown'
    post_title: str = 'Unknown'

    def __str__(self):
        return (
            f"[{self.subreddit}] -- Post Title: {'not yet retrieved' if not self.post_title_retrieved else self.post_title}\n"
            f"{self.body}\n"
            f"Author: {self.author} -- {self.created_time} -- {self.permalink}"
            )
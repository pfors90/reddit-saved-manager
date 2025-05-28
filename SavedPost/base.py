from dataclasses import dataclass
from datetime import datetime

@dataclass
class SavedPost:
    id: str
    author: str
    created_time: datetime
    permalink: str
    score: int
    subreddit: str
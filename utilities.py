from datetime import datetime
from selectors import SelectSelector
from typing import List, Dict, Tuple

from SavedPost import SavedComment, SavedSubmission

def parse_comment(praw_comment) -> SavedComment | None:
    if not praw_comment:
        return None

    comment = SavedComment(
        id = praw_comment.fullname,
        author = str(praw_comment.author) if praw_comment.author else "[author deleted]",
        body = praw_comment.body if praw_comment.body else "[no body content]",
        body_html = praw_comment.body_html if praw_comment.body_html else "<em>[no body content]</em>",
        created_time = datetime.fromtimestamp(praw_comment.created_utc),
        link_id = praw_comment.link_id,
        permalink = praw_comment.permalink,
        score = praw_comment.score,
        subreddit = str(praw_comment.subreddit)
    )

    return comment

def parse_comments(praw_comments):
    if not praw_comments:
        return []

    return [parse_comment(c) for c in praw_comments]

def parse_submission(praw_submission) -> SavedSubmission | None:
    if not praw_submission:
        return None

    submission = SavedSubmission(
        id = praw_submission.fullname,
        author = str(praw_submission.author) if praw_submission.author else "[author deleted]",
        created_time = datetime.fromtimestamp(praw_submission.created_utc),
        NSFW = praw_submission.over_18,
        permalink = praw_submission.permalink,
        score = praw_submission.score,
        subreddit = str(praw_submission.subreddit),
        title = praw_submission.title if praw_submission.title else "[no title]",
        upvote_ratio = praw_submission.upvote_ratio,
        url = praw_submission.url,
    )

    return submission

def parse_submissions(praw_submissions):
    if not praw_submissions:
        return []

    return [parse_submission(s) for s in praw_submissions]

# converts praw.model objects to custom SavedComment and SavedSubmission objects
# and pulls link_ids from comments to batch requests Submission objects via praw
# in order to populate SavedComment.post_title data member
# TODO -----
#  update to handle '[removed]' '[removed by reddit]' and '[deleted]' posts
#  we still want to store these in the database by ID to allow for bulk deletes
#  a la "spring cleaning" functionality
def parse_posts(app, praw_posts) -> Tuple[List[SavedComment], List[SavedSubmission]]:
    if not praw_posts:
        return [], []

    praw_comments = []
    praw_submissions = []

    for item in praw_posts:
        if item.fullname.startswith("t1"):
            praw_comments.append(item)
        elif item.fullname.startswith("t3"):
            praw_submissions.append(item)
        else:
            print("Error parsing item: " + item.fullname)

    saved_comments = parse_comments(praw_comments)
    saved_submissions = parse_submissions(praw_submissions)

    comment_link_ids = list({c.link_id for c in saved_comments})

    # initialize empty dict to ensure its empty
    post_ids_titles = dict()

    comment_submissions = app.reddit.get_submissions_by_ids(comment_link_ids)
    for submission in comment_submissions:
        # use getattr to handle cases where data may be malformed
        fullname = getattr(submission, "fullname", None)
        title = getattr(submission, "title", None)

        # populate_comment_post_titles handles missing post titles, so we
        # only need to care that it has a fullname
        if fullname:
            post_ids_titles[fullname] = title

    populate_comment_post_titles(saved_comments, post_ids_titles)

    return saved_comments, saved_submissions

def populate_comment_post_titles(comments: List[SavedComment], post_titles: Dict[str, str]):
    for comment in comments:
        if not comment.post_title_retrieved and comment.post_title == "Unknown":
            title = post_titles.get(comment.link_id)
            if title:
                comment.post_title = title
            else:
                comment.post_title = "Submission not found [link ID: " + comment.link_id + "]"

            comment.post_title_retrieved = True

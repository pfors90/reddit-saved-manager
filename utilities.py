from datetime import datetime
from typing import List, Dict

from SavedPost import SavedPost

def rewrap_comment(praw_post) -> SavedPost | None:
    if not praw_post or praw_post.fullname.split("_")[0] != "t1":
        return None

    post = SavedPost(
        id = praw_post.id,
        type = praw_post.fullname.split("_")[0],
        author = str(praw_post.author) if praw_post.author else "[author deleted]",
        body = getattr(praw_post, "body_html", "[no body content]"),
        created_time = datetime.fromtimestamp(praw_post.created_utc),
        link_id = getattr(praw_post, "link_id", "[no link]"),
        permalink = praw_post.permalink,
        score = praw_post.score,
        subreddit = str(praw_post.subreddit),
        NSFW = True,
        title = "[Unknown]",
        post_title_retrieved = False,
        url = "[no url]"
    )

    return post

def rewrap_submission(praw_post) -> SavedPost | None:
    if not praw_post:
        print(f"{praw_post.fullname} sent to rewrap_submission by mistake")
        return None

    post = SavedPost(
        id = praw_post.fullname,
        type = praw_post.fullname.split("_")[0],
        author = str(praw_post.author) if praw_post.author else "[author deleted]",
        body = getattr(praw_post, "selftext", "[no body content]"),
        created_time = datetime.fromtimestamp(praw_post.created_utc),
        link_id = praw_post.fullname,
        permalink = praw_post.permalink,
        score = praw_post.score,
        upvote_ratio = praw_post.upvote_ratio,
        subreddit = str(praw_post.subreddit),
        NSFW = getattr(praw_post, "over_18", True),
        title = getattr(praw_post, "title", "[no title]"),
        post_title_retrieved = True,
        url = getattr(praw_post, "url", "[no url]")
    )

    return post

def rewrap_post(praw_post):
    if praw_post.fullname.split("_")[0] == "t1":
        return rewrap_comment(praw_post)
    elif praw_post.fullname.split("_")[0] == "t3":
        return rewrap_submission(praw_post)

# converts praw.model objects to custom SavedPost objects and pulls link_ids
# from comments to batch requests Submission objects via praw in order to
# populate comment .title data member
# TODO -----
#  update to handle '[removed]' '[removed by reddit]' and '[deleted]' posts
#  we still want to store these in the database by ID to allow for bulk deletes
#  a la "spring cleaning" functionality
def parse_posts(app, praw_posts):
    if not praw_posts:
        return []

    saved_posts = [rewrap_post(p) for p in praw_posts]
    saved_comments = [p for p in saved_posts if p.type == "t1"]

    comment_link_ids = list({c.link_id for c in saved_comments})

    # initialize empty dict to ensure its empty
    posts_by_id = dict()

    comment_submissions = app.reddit.get_submissions_by_ids(comment_link_ids)

    for submission in comment_submissions:
        # use getattr to handle cases where data may be malformed
        fullname = getattr(submission, "fullname", None)

        # populate_comment_post_info and default values handle missing post titles, so we
        # only need to care that it has a fullname
        if fullname:
            posts_by_id[fullname] = submission

    if saved_comments is not None:
        populate_comment_post_info(saved_comments, posts_by_id)

    return saved_posts

def populate_comment_post_info(comments: List[SavedPost], posts_by_id: Dict[str, SavedPost]):
    for comment in comments:
        if not comment.post_title_retrieved and comment.title == "[Unknown]":
            post = posts_by_id.get(comment.link_id)
            if post:
                comment.NSFW = getattr(post, "over_18", True)
                comment.title = getattr(post, "title", "[no title]")
                comment.url = getattr(post, "url", "[no url]")

            comment.post_title_retrieved = True

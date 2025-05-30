from datetime import datetime
from typing import List, Dict

from SavedPost import SavedPost

def parse_post(praw_post) -> SavedPost | None:
    if not praw_post:
        return None

    post_type = praw_post.fullname.split("_")[0]

    # unnecessary duplication, but helps with readability
    is_comment = (post_type == "t1")
    is_post = (post_type == "t3")

    post = SavedPost(
        id = praw_post.fullname,
        type = post_type,
        author = str(praw_post.author) if praw_post.author else "[author deleted]",
        body = getattr(praw_post, "body", "[no body content]") or getattr(praw_post, "selftext", "[no body content]"),
        created_time = datetime.fromtimestamp(praw_post.created_utc),
        link_id = getattr(praw_post, "link_id", "[no link]") if is_comment else praw_post.fullname,
        permalink = praw_post.permalink,
        score = praw_post.score,
        subreddit = str(praw_post.subreddit),
        NSFW = getattr(praw_post, "over_18", True) if is_post else True,
        title = getattr(praw_post, "title", "[no title]") if is_post else "[Unknown]",
        post_title_retrieved = True if is_post else False,
        url = getattr(praw_post, "url", "[no url]") if is_post else "[no url]"
    )

    return post

# converts praw.model objects to custom SavedPost objects and pulls link_ids
# from comments to batch requests Submission objects via praw in order to
# populate comment .post_title data member
# TODO -----
#  update to handle '[removed]' '[removed by reddit]' and '[deleted]' posts
#  we still want to store these in the database by ID to allow for bulk deletes
#  a la "spring cleaning" functionality
def parse_posts(app, praw_posts):
    if not praw_posts:
        return []

    saved_posts = [parse_post(p) for p in praw_posts]
    saved_comments = list({p for p in saved_posts if p.type == "t1"})

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

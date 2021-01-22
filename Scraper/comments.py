import config
import praw
import database


def scrape_comments(post):
    errors = {}
    # Initialise DB Persistance
    cxn = database.connection()
    cxn.connect()
    # Initialise Reddit
    reddit = praw.Reddit(client_id=config.reddit_client_id,
                         client_secret=config.reddit_client_secret,
                         user_agent='python:com.comment_bot:0.1 (by /u/popeus)',
                         user=config.reddit_user,
                         password=config.reddit_password)

    # Scrape Comments
    submission = reddit.submission(id=post)
    submission.comment_sort = 'new'
    for comment in submission.comments:
        try:
            #Skip deleted comments, they're trash
            if comment is not None and comment.author is not None:
                cxn.insert_comment(comment_id=comment.id,
                                   post_id=post,
                                   body=comment.body,
                                   upvotes=comment.ups,
                                   downvotes=comment.downs,
                                   score=comment.score,
                                   author=comment.author.name,
                                   created_epoch=comment.created_utc,
                                   post_permalink=comment.permalink)
        except Exception as e:
            errors = {comment.id:e}
    cxn.update_post_as_processed(post_id=post)
    cxn.disconnect()
    return errors



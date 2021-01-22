import praw
import config
from datetime import datetime
import database


def scrape_posts(subreddit):

    # Initialise DB Persistence & variables
    cxn = database.connection()
    cxn.connect()
    reddit = praw.Reddit(client_id=config.reddit_client_id,
                         client_secret=config.reddit_client_secret,
                         user_agent='python:com.comment_bot:0.1 (by /u/popeus)',
                         user=config.reddit_user,
                         password=config.reddit_password)

    # If this is a new Subreddit, insert it into the table
    if len(cxn.get_subreddit_by_id(subreddit)) == 0:
        print('First scrape of r/' + subreddit)
        cxn.insert_subreddit(subreddit, reddit.subreddit(subreddit)._path)

    #If this sub has never been scraped before, scrape data back to 1 Jan 2016.
    if cxn.get_number_of_posts(subreddit) == 0:
        start_date = datetime(2016,1,1,0,0)
        end_date = datetime.now().timestamp()
    #Otherwise, scrape data since the last post to today.
    else:
        start_date = cxn.get_latest_post(subreddit)[0]+1
        end_date = datetime.now().timestamp()

    print('Scraping Posts from {0} to {1} from r/{2}.'.format(datetime.fromtimestamp(end_date),
                                                              datetime.fromtimestamp(start_date), subreddit))

    for submission in reddit.subreddit(subreddit).submissions(start=start_date, end=end_date):
        try:
            cxn.insert_post(ID=submission.id,
                            subreddit_name=subreddit,
                            title=submission.title,
                            upvotes=submission.ups,
                            downvotes=submission.downs,
                            score=submission.score,
                            author=submission.author.name,
                            created_epoch=submission.created_utc,
                            permalink=submission.permalink)
        except Exception as e:
            print(e)
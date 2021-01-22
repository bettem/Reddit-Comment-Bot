from multiprocessing import Pool

from tqdm import tqdm

import database
from Scraper.comments import scrape_comments
from Scraper.posts import scrape_posts

if __name__ == '__main__':
    #Variables
    subreddit = 'aww'

    #Srape new posts from the subreddit
    scrape_posts(subreddit)

    #Scrape the top level comments on those posts
    print('Scraping top level comments on posts.')
    cxn = database.connection()
    cxn.connect()
    posts = cxn.get_posts_to_process(subreddit)

    pool = Pool(processes=64)
    while posts:
        try:
            for _ in tqdm(pool.imap_unordered(scrape_comments, posts), total=len(posts), unit='posts'):
                pass
            posts = cxn.get_posts_to_process(subreddit)
        #Common to get memory issue due to multi threading.
        except Exception as e:
             print(e)
    pool.close()
    pool.join()
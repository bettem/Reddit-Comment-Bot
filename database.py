import pyodbc

import config


class connection():
    def __init__(self):
        self.user = config.db_user
        self.password = config.db_password
        self.database = config.db_database
        self.server = config.db_server

    def connect(self):
        self.cnxn = pyodbc.connect(
            'Driver={SQL Server};Server=' + self.server + ';database=' + self.database + ';uid=' + self.user + ';pwd=' + self.password + '')
        self.cursor = self.cnxn.cursor()

    def insert_subreddit(self, name, short_url):
        SQLCommand = "INSERT INTO dbo.Subreddits(Subreddit_ID, Subreddit_Short_URL) VALUES(?,?)"
        Values = name, short_url
        self.cursor.execute(SQLCommand, Values)
        self.cnxn.commit()

    def get_subreddit_by_id(self, name):
        rows = []
        SQLCommand = "SELECT Subreddit_ID, Subreddit_Short_URL, Subreddit_Full_URL FROM dbo.Subreddits WHERE Subreddit_ID  = ?"
        Values = [name]
        self.cursor.execute(SQLCommand, Values)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            rows.append(row)
        return rows

    def get_earliest_post(self, subreddit):
        rows = []
        SQLCommand = "SELECT ISNULL(MIN(Created_Epoch),DATEDIFF(S,'1 Jan 1970',GETDATE()))-10 AS Earliest_Post "  \
                     "FROM dbo.Posts WHERE Subreddit_ID = ?"
        Values = [subreddit]
        self.cursor.execute(SQLCommand, Values)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            rows.append(row.Earliest_Post)
        return rows

    def get_latest_post(self, subreddit):
        rows = []
        SQLCommand = "SELECT MAX(Created_Epoch) AS Latest_Post "  \
                     "FROM dbo.Posts WHERE Subreddit_ID = ?"
        Values = [subreddit]
        self.cursor.execute(SQLCommand, Values)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            rows.append(row.Latest_Post)
        return rows

    def get_number_of_posts(self, subreddit):
        rows = []
        SQLCommand = "SELECT ISNULL(COUNT(*),0) AS Num_Posts "  \
                     "FROM dbo.Posts WHERE Subreddit_ID = ?"
        Values = [subreddit]
        self.cursor.execute(SQLCommand, Values)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            rows.append(row.Num_Posts)
        return rows

    def insert_post(self, ID, subreddit_name, title, upvotes, downvotes, score, author, created_epoch, permalink):
        SQLCommand = "INSERT INTO dbo.Posts (Post_ID, Subreddit_ID, Title, Upvotes, Downvotes, Score, Author, Created_Epoch, Post_Permalink)" \
                     "VALUES (?,?,?,?,?,?,?,?,?)"
        Values = [ID, subreddit_name, title, upvotes, downvotes, score, author, created_epoch, permalink]
        self.cursor.execute(SQLCommand, Values)
        self.cnxn.commit()

    def insert_comment(self, comment_id, post_id, body, upvotes, downvotes, score, author, created_epoch, post_permalink):
        SQLCommand = "exec dbo.sp_Insert_Comment ?,?,?,?,?,?,?,?,?"
        Values = [comment_id, post_id, body, upvotes, downvotes, score, author, created_epoch, post_permalink]
        self.cursor.execute(SQLCommand, Values)
        self.cnxn.commit()

    def update_post_as_processed(self, post_id):
        SQLCommand = "UPDATE dbo.Posts SET Comments_Processed_Flag = 1 WHERE Post_ID = ?"
        Values = [post_id]
        self.cursor.execute(SQLCommand, Values)
        self.cnxn.commit()

    def get_posts_to_process(self, subreddit_name):
        rows = []
        SQLCommand = "SELECT TOP 10000 Post_ID FROM dbo.Posts WHERE Subreddit_ID = ? AND Comments_Processed_Flag = 0"
        Values = [subreddit_name]
        self.cursor.execute(SQLCommand, Values)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            rows.append(row.Post_ID)
        return rows

    def get_popular_comments(self, subreddit_name):
        rows = []
        SQLCommand = "SELECT TOP 250000 C.Body AS Comment " \
                     ",P.Title as Post_Title " \
                     "FROM dbo.Comments C " \
                     "INNER JOIN dbo.Posts P ON P.Post_ID = C.Post_ID " \
                     "WHERE P.Subreddit_ID = ? and C.score > 0 and P.Score > 0" \
                     "AND C.Body NOT LIKE '%http%' and P.Title NOT LIKE '%http%'" \
                     "ORDER BY C.Score DESC"
        Values = [subreddit_name]
        self.cursor.execute(SQLCommand, Values)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            rows.append([row.Post_Title,row.Comment])
        return rows

    def disconnect(self):
        self.cnxn.close()

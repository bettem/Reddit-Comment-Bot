USE CommentBot
GO
DROP TABLE IF EXISTS dbo.Subreddits
GO
CREATE TABLE dbo.Subreddits (
  Subreddit_ID         NVARCHAR(128) PRIMARY KEY CLUSTERED NOT NULL,
  Subreddit_Short_URL  NVARCHAR(256)                       NOT NULL,
  Subreddit_Full_URL AS CONCAT('https://www.reddit.com', Subreddit_Short_URL),
  Last_Update_User     NVARCHAR(128) DEFAULT SUSER_NAME()  NOT NULL,
  Last_Update_Datetime DATETIME2 DEFAULT GETDATE()         NOT NULL
)
DROP TABLE IF EXISTS dbo.Posts
GO
CREATE TABLE dbo.Posts (
  Post_ID              NVARCHAR(128) PRIMARY KEY CLUSTERED NOT NULL,
  Subreddit_ID         NVARCHAR(128)                       NOT NULL,
  Title                NVARCHAR(512)                       NOT NULL,
  Upvotes              INT                                 NOT NULL,
  Downvotes            INT                                 NOT NULL,
  Score                INT                                 NOT NULL,
  Author               NVARCHAR(256)                       NOT NULL,
  Created_Epoch        BIGINT                              NOT NULL,
  Created_Datetime    AS DATEADD(S, Created_Epoch, '1 Jan 1970'),
  Post_Permalink       NVARCHAR(256)                       NOT NULL,
  Post_Full_Permalink AS CONCAT('https://www.reddit.com', Post_Permalink),
  Last_Update_User     NVARCHAR(128) DEFAULT SUSER_NAME()  NOT NULL,
  Last_Update_Datetime DATETIME2 DEFAULT GETDATE()         NOT NULL
)
GO
DROP TABLE IF EXISTS dbo.Comments
GO
CREATE TABLE dbo.Comments (
  Comment_ID           NVARCHAR(128) PRIMARY KEY CLUSTERED NOT NULL,
  Body                 NVARCHAR(MAX)                       NULL,
  Upvotes              INT                                 NOT NULL,
  Downvotes            INT                                 NOT NULL,
  Score                INT                                 NOT NULL,
  Author               NVARCHAR(256)                       NOT NULL,
  Created_Epoch        BIGINT                              NOT NULL,
  Created_Datetime    AS DATEADD(S, Created_Epoch, '1 Jan 1970'),
  Post_Permalink       NVARCHAR(256)                       NOT NULL,
  Post_Full_Permalink AS CONCAT('https://www.reddit.com', Post_Permalink),
  Last_Update_User     NVARCHAR(128) DEFAULT SUSER_NAME()  NOT NULL,
  Last_Update_Datetime DATETIME2 DEFAULT GETDATE()         NOT NULL
)
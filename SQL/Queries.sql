SELECT P.Post_ID
      ,COUNT(C.Comment_ID) AS Number_Of_Comments
FROM dbo.Comments C
INNER JOIN dbo.Posts P ON
            P.Post_ID = C.Post_ID
WHERE P.Comments_Processed_Flag = 1
GROUP BY  P.Post_ID
ORDER BY 2 DESC;


SELECT COUNT(DISTINCT P.Post_ID) AS [Total Posts]
      ,COUNT(DISTINCT IIF(P.Comments_Processed_Flag = 1,P.Post_ID,NULL)) AS [Posts Processed]
      ,COUNT(DISTINCT IIF(C.Comment_ID IS NOT NULL, P.Post_ID, NULL)) AS [Posts with Comments]
      ,COUNT(C.Comment_ID) as [Total Comments]
FROM dbo.Posts P
LEFT JOIN dbo.Comments C ON
            P.Post_ID = C.Post_ID;

SELECT COUNT(DISTINCT  Post_ID) FROM dbo.Comments;



SELECT TOP 1000 *
FROM dbo.Comments
ORDER BY Score ASC
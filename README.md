#### Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
Designed database provides for central data source for information otherwise available 
in semi-structured format: users interactions with application, enriched with songs and artists information. 

#### State and justify your database schema design and ETL pipeline.
**Schema**

We defined four dimension tables: `users` describing users of our application, 
`songs`, `artists` providing additional information about streamed data in our application,
finally `time` helper table, which purpose could be making time aggregations of song plays easier.

**ETL pipeline** 

Processing is composed of three main steps:
- extracting data, iterating, listing and reading content of individual files from the source directory
- transforming individual file data into structures compatible with the designed schema
- loading transformed data into correct tables

#### [Optional] Provide example queries and results for song play analysis.
```
-- most active users
SELECT u.first_name || ' ' || u.last_name as user, count(1)
FROM songplays sp
         JOIN time t ON sp.start_time = t.start_time
         JOIN users u ON sp.user_id = u.user_id
GROUP BY 1
ORDER BY 2 DESC;

-- which gender is more active
SELECT u.gender, count(1)
FROM songplays sp
         JOIN time t ON sp.start_time = t.start_time
         JOIN users u ON sp.user_id = u.user_id
GROUP BY 1
ORDER BY 2 DESC;

-- which subscription level is more active
SELECT u.level, count(1)
FROM songplays sp
         JOIN time t ON sp.start_time = t.start_time
         JOIN users u ON sp.user_id = u.user_id
GROUP BY 1
ORDER BY 2 DESC;

-- days of week with most songs plays
SELECT weekday, count(1)
FROM songplays sp
     JOIN time t ON sp.start_time = t.start_time
GROUP BY 1
ORDER BY 2 DESC;
```
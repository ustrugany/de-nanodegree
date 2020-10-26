# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_table_create = ("""
CREATE TABLE songplays (songplay_id serial primary key, start_time timestamp, user_id int, level varchar, song_id int, artist_id int, session_id int, user_agent varchar);
""")

# users - users in the app
user_table_create = ("""
CREATE TABLE users (user_id int, first_name varchar, last_name varchar, gender char(1), level varchar);
CREATE UNIQUE INDEX users_unique_1 ON users(user_id);
""")

# songs - songs in music database
song_table_create = ("""
CREATE TABLE songs (song_id varchar, title varchar, artist_id varchar, year int, duration numeric(10,5))
""")

# artist_id, name, location, latitude, longitude
artist_table_create = ("""
CREATE TABLE artists (artist_id varchar, name varchar, location varchar, latitude numeric(12, 8), longitude numeric(12, 8))
""")

# time - timestamps of records in songplays broken down into specific units
time_table_create = ("""
CREATE TABLE time (start_time timestamp, hour int, day int, week int, month int, year int, weekday int)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level = users.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id from songs s join artists a ON s.artist_id = a.artist_id 
WHERE LOWER(s.title) LIKE LOWER(%s) AND (a.name) LIKE LOWER(%s) AND ROUND(s.duration, 3) = ROUND(%s, 3);
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
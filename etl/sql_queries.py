# DROP TABLES

songplays_table_drop = "DROP TABLE IF EXISTS songplays;"
users_table_drop = "DROP TABLE IF EXISTS users;"
songs_table_drop = "DROP TABLE IF EXISTS songs"
artists_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# songplays - records in log data associated with song plays i.e. records with page NextSong
songplays_table_create = ("""
CREATE TABLE songplays (
    songplay_id serial primary key,
    start_time timestamp not null,
    user_id int not null, 
    level varchar,
    song_id varchar,
    artist_id varchar,
    session_id int,
    user_agent varchar
);
ALTER TABLE songplays ADD CONSTRAINT songplays_users_fk FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE songplays ADD CONSTRAINT songplays_songs_fk FOREIGN KEY (song_id) REFERENCES songs(song_id);
ALTER TABLE songplays ADD CONSTRAINT songplays_artists_fk FOREIGN KEY (artist_id) REFERENCES artists(artist_id);
""")

# users - users in the app
users_table_create = ("""
CREATE TABLE users (
    user_id int primary key, 
    first_name varchar, 
    last_name varchar, 
    gender char(1), 
    level varchar
);
""")

# songs - songs in music database
songs_table_create = ("""
CREATE TABLE songs (
    song_id varchar primary key, 
    title varchar, 
    artist_id varchar, 
    year int, 
    duration numeric(10,5)
);
""")

# artists
artists_table_create = ("""
CREATE TABLE artists (
    artist_id varchar primary key, 
    name varchar, 
    location varchar, 
    latitude numeric(12, 8), 
    longitude numeric(12, 8)
);
""")

# time - timestamps of records in songplays broken down into specific units
time_table_create = ("""
CREATE TABLE time (
    start_time timestamp primary key, 
    hour int not NULL, 
    day int not NULL, 
    week int not NULL, 
    month int not NULL, 
    year int not NULL, 
    weekday int not NULL
);
""")

# INSERT RECORDS

songplays_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

users_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level = excluded.level;
""")

songs_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (song_id) DO NOTHING;
""")

artists_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT
    s.song_id
    , a.artist_id 
FROM songs s 
JOIN artists a 
ON s.artist_id = a.artist_id 
WHERE LOWER(s.title) LIKE LOWER(%s) 
    AND (a.name) LIKE LOWER(%s) 
    AND ROUND(s.duration, 3) = ROUND(%s, 3);
""")

# QUERY LISTS

create_table_queries = [users_table_create, songs_table_create, artists_table_create, time_table_create,
                        songplays_table_create]
drop_table_queries = [songplays_table_drop, users_table_drop, songs_table_drop, artists_table_drop, time_table_drop]
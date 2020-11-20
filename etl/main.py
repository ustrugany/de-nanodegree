import os
import glob
from typing import List, Tuple, Callable

import psycopg2
import pandas as pd
import json

from psycopg2 import extensions
from psycopg2._psycopg import connection

from sql_queries import songs_table_insert, artists_table_insert, time_table_insert, users_table_insert, song_select, \
    songplays_table_insert


def process_song_file(cur: extensions.cursor, filepath: str):
    """
    Function reads a file of songs data. Saves songs and artists information into corresponding tables.
    :param cur: connection cursor
    :param filepath: filepath to the file with songs data
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data, index=[0])

    song_df = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = song_df.values
    song_data = song_data[0]
    song_data = song_data.tolist()
    cur.execute(songs_table_insert, song_data)

    artist_df = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_df.values
    artist_data = artist_data[0]
    artist_data = artist_data.tolist()
    cur.execute(artists_table_insert, artist_data)


def process_log_file(cur: extensions.cursor, filepath: str):
    """
    Function reads a file of logs data. Filters data only to "NextSong" action.
    Breaks timestamps of records in songplays down into specific units and saves in helper table.
    Saves users and songplay information in corresponding tables.

    :param cur: connection cursor
    :param filepath: filepath to the file with songs data
    """

    data: List = []
    with open(filepath, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                data.append(json.loads(line))

    df = pd.DataFrame(data)

    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df['ts']
    t = pd.to_datetime(t, unit='ms')

    time_data = (
        t.dt.tz_localize('UTC').values,
        t.dt.hour.tolist(),
        t.dt.day.tolist(),
        t.dt.week.tolist(),
        # t.dt.isocalendar().week.tolist(),
        t.dt.month.tolist(),
        t.dt.year.tolist(),
        t.dt.weekday.tolist()
    )
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    for i, row in user_df.iterrows():
        cur.execute(users_table_insert, row)

    for index, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

        d = pd.to_datetime(row.ts, unit='ms')
        start_time, user_id, level, session_id, user_agent = d.tz_localize('UTC'), row.userId, row.level, row.sessionId, row.userAgent
        songplay_data: Tuple = (start_time, user_id, level, song_id, artist_id, session_id, user_agent)
        cur.execute(songplays_table_insert, songplay_data)


def process_data(cur: extensions.cursor, conn: connection, filepath: str, func: Callable):
    """
    Function reads all *.json files in a directory, resolving it's absolut path and
        appending to a list.
    Prints out total number of found files and finally processes each them calling passed in callback.

    :param cur: connection cursor
    :param conn: connection object
    :param filepath: filepath to the directory with songs or logs data
    :param func: callback function to process single data file: songs or logs
    """

    all_files: List = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files: int = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=postgres dbname=sparkifydb user=udacity password=udacity")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
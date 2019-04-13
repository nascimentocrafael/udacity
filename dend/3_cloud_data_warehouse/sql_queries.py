import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# CREATE SCHEMAS

fact_schema= ("CREATE SCHEMA IF NOT EXISTS fact_tables")
dimension_schema= ("CREATE SCHEMA IF NOT EXISTS dimension_tables")
staging_schema= ("CREATE SCHEMA IF NOT EXISTS staging_tables")

# DROP SCHEMAS

fact_schema_drop= ("DROP SCHEMA IF EXISTS fact_tables CASCADE")
dimension_schema_drop= ("DROP SCHEMA IF EXISTS dimension_tables CASCADE")
staging_schema_drop= ("DROP SCHEMA IF EXISTS staging_tables CASCADE")


# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_tables.staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_tables.staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS fact_tables.songplays"
user_table_drop = "DROP TABLE IF EXISTS dimension_tables.users"
song_table_drop = "DROP TABLE IF EXISTS dimension_tables.songs"
artist_table_drop = "DROP TABLE IF EXISTS dimension_tables.artists"
time_table_drop = "DROP TABLE IF EXISTS dimension_tables.time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_tables.staging_events 
                                                                (event_id INT IDENTITY(0,1), 
                                                                artist VARCHAR(200), 
                                                                auth VARCHAR(100), 
                                                                first_name VARCHAR(100), 
                                                                gender VARCHAR(10), 
                                                                item_session INT, 
                                                                last_name VARCHAR(100), 
                                                                length NUMERIC, 
                                                                level VARCHAR(10), 
                                                                location VARCHAR(500), 
                                                                method VARCHAR(10), 
                                                                page VARCHAR(100), 
                                                                registration NUMERIC, 
                                                                session_id INT, 
                                                                song VARCHAR(200), 
                                                                status INT, 
                                                                ts BIGINT, 
                                                                user_agent VARCHAR(500), 
                                                                user_id INT,
                                                                PRIMARY KEY (event_id)) 
                                                                DISTSTYLE ALL""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_tables.staging_songs 
                                                                (num_songs INT, 
                                                                artist_id VARCHAR(50), 
                                                                artist_latitude VARCHAR(50), 
                                                                artist_longitude VARCHAR(50), 
                                                                artist_location VARCHAR(500), 
                                                                artist_name VARCHAR(500), 
                                                                song_id VARCHAR(50), 
                                                                title VARCHAR(500), 
                                                                duration NUMERIC, 
                                                                year INT,
                                                                PRIMARY KEY (song_id)) 
                                                                DISTSTYLE ALL""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS fact_tables.songplays 
                                                                (songplay_id INT IDENTITY(0,1), 
                                                                start_time TIMESTAMP NOT NULL, 
                                                                user_id INT NOT NULL, 
                                                                level VARCHAR(10) NOT NULL, 
                                                                song_id VARCHAR(50), 
                                                                artist_id VARCHAR(50), 
                                                                session_id INT NOT NULL, 
                                                                location VARCHAR(500) NOT NULL, 
                                                                user_agent VARCHAR(500) NOT NULL,
                                                                PRIMARY KEY(songplay_id),
                                                                FOREIGN KEY(user_id) REFERENCES dimension_tables.users(user_id),
                                                                FOREIGN KEY(song_id) REFERENCES dimension_tables.songs(song_id),
                                                                FOREIGN KEY(artist_id) REFERENCES dimension_tables.artists(artist_id),
                                                                FOREIGN KEY(start_time) REFERENCES dimension_tables.time(start_time))
                                                                DISTSTYLE ALL""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS dimension_tables.users 
                                                        (user_id INT NOT NULL, 
                                                        first_name VARCHAR(100), 
                                                        last_name VARCHAR(100), 
                                                        gender VARCHAR(10), 
                                                        level VARCHAR(10) NOT NULL,
                                                        PRIMARY KEY (user_id)) 
                                                        DISTSTYLE ALL""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS dimension_tables.songs 
                                                        (song_id VARCHAR(50) NOT NULL, 
                                                        title VARCHAR(500) NOT NULL, 
                                                        artist_id VARCHAR(50) NOT NULL, 
                                                        year INT, 
                                                        duration NUMERIC,
                                                        PRIMARY KEY (song_id)) 
                                                        DISTSTYLE ALL""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS dimension_tables.artists 
                                                            (artist_id VARCHAR(50) NOT NULL, 
                                                            name VARCHAR(500) NOT NULL, 
                                                            location VARCHAR(500), 
                                                            latitude NUMERIC, 
                                                            longitude NUMERIC,
                                                            PRIMARY KEY (artist_id)) 
                                                            DISTSTYLE ALL""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS dimension_tables.time 
                                                       (start_time TIMESTAMP, 
                                                       hour INT, 
                                                       day INT, 
                                                       week INT, 
                                                       month INT, 
                                                       year INT, 
                                                       weekday INT,
                                                       PRIMARY KEY (start_time)) 
                                                       DISTSTYLE ALL""")

# STAGING TABLES

staging_events_copy = ("copy {} from {} credentials 'aws_iam_role={}' region as 'us-west-2' format as json {};").format('staging_tables.staging_events', 
                                                                                                       config.get("S3","LOG_DATA"),
                                                                                                       config.get("IAM_ROLE","ARN"),
                                                                                                       config.get("S3","LOG_JSONPATH"))

staging_songs_copy = ("copy {} from {} credentials 'aws_iam_role={}' region as 'us-west-2' json 'auto';").format('staging_tables.staging_songs', 
                                                                                                       config.get("S3","SONG_DATA"),
                                                                                                       config.get("IAM_ROLE","ARN"))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO fact_tables.songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 Second '    AS start_time, 
	                               se.user_id                                               AS user_id, 
                                   se.level                                                 AS level, 
                                   ds.song_id                                               AS song_id, 
                                   da.artist_id                                             AS artist_id, 
                                   se.session_id                                            AS session_id, 
                                   se.location                                              AS location,  
                                   se.user_agent                                            AS user_agent 
                            FROM staging_tables.staging_events se 
                            JOIN dimension_tables.songs ds ON (ds.title = se.song AND ROUND(ds.duration, 2) = ROUND(se.length, 2)) 
                            JOIN dimension_tables.artists da ON  (da.name = se.artist)
                            WHERE se.page = 'NextSong';""")

user_table_insert = ("""INSERT INTO dimension_tables.users (user_id, first_name, last_name, gender, level) 
                      SELECT DISTINCT se.user_id    AS user_id, 
                                      se.first_name AS first_name, 
                                      se.last_name  AS last_name, 
                                      se.gender     AS gender, 
                                      se.level      AS level 
                      FROM staging_tables.staging_events se
                      WHERE se.page = 'NextSong';""")

song_table_insert = ("""INSERT INTO dimension_tables.songs (song_id, title, artist_id, year, duration) 
                      SELECT DISTINCT ss.song_id    AS song_id, 
                                      ss.title      AS title, 
                                      ss.artist_id  AS artist_id, 
                                      ss.year       AS year, 
                                      ss.duration   AS duration 
                      FROM staging_tables.staging_songs ss;""")

artist_table_insert = ("""INSERT INTO dimension_tables.artists (artist_id, name, location, latitude, longitude) 
                        SELECT DISTINCT ss.artist_id AS artist_id, 
                               ss.artist_name        AS name,  
                               ss.artist_location    AS location, 
                               ss.artist_latitude    AS latitude, 
                               ss.artist_longitude   AS longitude 
                        FROM staging_tables.staging_songs ss;""")

time_table_insert = ("""INSERT INTO dimension_tables.time (start_time, hour, day, week, month, year, weekday)
                        SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 Second '  AS start_time, 
		                                EXTRACT(hour FROM start_time)                       AS hour,
		                                EXTRACT(day FROM start_time)                        AS day, 
                                        EXTRACT(week FROM start_time)                       AS week,
                                        EXTRACT(month FROM start_time)                      AS month, 
                                        EXTRACT(year FROM start_time)                       AS year,
                                        EXTRACT(weekday FROM start_time)                    AS weekday
                        FROM staging_tables.staging_events;""")

# QUERY LISTS

create_schemas_queries = [fact_schema, dimension_schema, staging_schema]
drop_schemas_queries = [fact_schema_drop, dimension_schema_drop, staging_schema_drop]
create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, songplay_table_insert, time_table_insert]

# Project Description

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides into a S3 bucket on AWS in the form of JSON files. One of them logs user activity on the app, and the other the metadata on the songs in their app.

Our goal here was to craete a dimensional model, star schema, in order to facilitate analysis.  By doing so, the data science team will be able to easily see what are the most streamed songs and artists. This is specially good because with that information the startup Sparkify can better remunerate their artists. Can also improve those artists repertories , i.e include more songs of that artist. Can make contact with similar artists to be part of their music streaming app. Can also improve their recommendation algorithm to recommend song to users. The possibilities are really huge.

The first thing to do was to create staging tables to copy data from S3 to redshift. Those tables are 'staging_events' for log data and 'staging_songs' for metadata on the songs.

In order to better organize the project tables, it was created three schemas, the 'staging_tables' schema, 'dimension_tables' schema and 'fact_tables' schema.

# Staging Tables

- staging_events - log files data.
   - event_id
   - artist
   - auth
   - first_name
   - gender
   - item_session
   - last_name
   - length
   - level
   - location
   - method
   - page
   - registration
   - session_id
   - song 
   - status
   - ts
   - user_agent
   - user_id


- staging_songs - songs' metadata files data.
   - num_songs
   - artist_id
   - artist_latitude
   - artist_longitude
   - artist_location
   - artist_name
   - song_id
   - title
   - duration
   - year

# Dimensional Model

Our model is formed by 1 fact table 'songplays' and 4 dimension tables 'users', 'songs', 'artists' and 'time'. With this model we are able to easily make analisys of users and their favority songs and artists. 

The dimension tables helps to reduce duplication for songs and artists tables, for example. Because this way you have all the songs data in on songs table and all the artists data in one artists table.

## Fact Table

- songplays - records in log data associated with song plays i.e. records with page NextSong
   - songplay_id
   - start_time
   - user_id
   - level
   - song_id
   - artist_id
   - session_id
   - location
   - user_agent

## Dimension Tables

- users - users in the app
   - user_id
   - first_name
   - last_name
   - gender
   - level
 
 
- songs - songs in music database
   - song_id
   - title
   - artist_id
   - year
   - duration
 
 
- artists - artists in music database
   - artist_id
   - name
   - location
   - lattitude
   - longitude
    
    
- time - timestamps of records in songplays broken down into specific units
   - start_time
   - hour, day
   - week
   - month
   - year
   - weekday


# Files

- create_tables.py - python script with functions to create the databese and create and drop schemas and tables given a query.

- sql_queries.py - python script with the queries used in the project. These queries drop, create, copy and insert.

- etl.py - ETL pipeline created to extract, transform and load the data to our tables and star schema.

- dwh.cfg - Redshift's parameters file.

- README.md - this file.

# Executing The Project

1. Run the script to create tables. Open a console and do the following:

```shell
$ python create_tables.py
```

2. Run the ETL script. In the console, do the following:

```shell
$ python etl.py
```


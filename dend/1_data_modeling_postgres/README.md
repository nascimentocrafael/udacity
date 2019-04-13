# Project Description

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Our goal here was to craete a dimensional model, star schema, in order to facilitate analysis.  By doing so, the data science team will be able to easily see what are the most streamed songs and artists. This is specially good because with that information the startup Sparkify can better remunerate their artists. Can also improve those artists repertories , i.e include more songs of that artist. Can make contact with similar artists to be part of their music streaming app. Can also improve their recommendation algorithm to recommend song to users. The possibilities are really huge.

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

- create_tables.py - python script with functions to create the databese and create and drop tables given a query.

- sql_queries.py - python script with the queries used in the project. These queries include, drop, create, insert and select.

- etl.ipynb - jupyter notebook used to experiment with the data and test the queries.

- test.ipynb - jypyter notebook used to test the code and see the state of the database.

- etl.py - ETL pipeline created to extract, transform and load the data from all files to our star schema.

- data - folder with the files used.

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

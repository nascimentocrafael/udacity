import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
import time

def load_staging_tables(cur, conn):
    '''
    Function to load staging tables. It performs a S3 COPY command. This function uses the variable 'copy_table_queries' defined in the 'sql_queries.py' file.
    Parameters:
        - curr: Cursor for a database connection
        - conn: Database connection
    Outputs:
        None
    '''
    for query in copy_table_queries:
        start = time.time()
        print("Executing query: \n {}".format(query))
        cur.execute(query)
        conn.commit()
        end = time.time()
        print("elapsed time: {} \n".format(end-start))


def insert_tables(cur, conn):
    '''
    Function to insert data into dimension and fact tables. This function uses the variable 'insert_table_queries' defined in the 'sql_queries.py' file.
    Parameters:
        - curr: Cursor for a database connection
        - conn: Database connection
    Outputs:
        None
    '''
    for query in insert_table_queries:
        start = time.time()
        print("Executing query: \n {}".format(query))
        cur.execute(query)
        conn.commit()
        end = time.time()
        print("elapsed time: {} \n".format(end-start))


def main():
    '''
    Main function. Read and parses configuration file 'dwh.cfg', create the connection and call the functions to insert data into stages, dimension and fact tables.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

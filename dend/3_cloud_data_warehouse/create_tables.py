import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, create_schemas_queries, drop_schemas_queries


def drop_tables(cur, conn):
    '''
    Function to drop tables. This function uses the variable 'drop_table_queries' defined in the 'sql_queries.py' file.
    Parameters:
        - curr: Cursor for a database connection
        - conn: Database connection
    Outputs:
        None
    '''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    '''
    Function to create tables. This function uses the variable 'create_table_queries' defined in the 'sql_queries.py' file.
    Parameters:
        - curr: Cursor for a database connection
        - conn: Database connection
    Outputs:
        None
    '''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def create_schemas(cur, conn):
    '''
    Function to create schemas. This function uses the variable 'create_schemas_queries' defined in the 'sql_queries.py' file.
    Parameters:
        - curr: Cursor for a database connection
        - conn: Database connection
    Outputs:
        None
    '''
    for query in create_schemas_queries:
        cur.execute(query)
        conn.commit()        

def drop_schemas(cur, conn):
    '''
    Function to drop schemas. This function uses the variable 'drop_schemas_queries' defined in the 'sql_queries.py' file.
    Parameters:
        - curr: Cursor for a database connection
        - conn: Database connection
    Outputs:
        None
    '''
    for query in drop_schemas_queries:
        cur.execute(query)
        conn.commit()
        
def main():
    '''
    Main function. Read and parses configuration file 'dwh.cfg', create the connection and call the functions to drop/create schemas and tables.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    try:
        drop_schemas(cur, conn)
        print("Schemas Droped")
    except:
        print("No schemas to drop")

    try:
        create_schemas(cur, conn)
        print("Schemas Created")
    except:
        print("Could not create schemas")

    try:
        create_tables(cur, conn)
        print("Tables Created")
    except:
        print("Could not create tables")

    conn.close()

if __name__ == "__main__":
    main()

import psycopg2
from psycopg2 import Error
import pandas.io.sql as sqlio

#query function
def do_query(query, user, password, host, port, database):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        
        # Create a cursor to perform database operations
        cursor = connection.cursor()
            
        #Query 1
        postgreSQL_select_Query = query
        result_query=sqlio.read_sql_query(postgreSQL_select_Query, connection)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return result_query




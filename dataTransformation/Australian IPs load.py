import mysql.connector
import configparser
import os
import pandas as pd

############################################### Local

mysql_host = 'localhost'
mysql_port='8157'
mysql_user = 'devCrcDbAdmin'
mysql_password = 'sjigjRiQfHVfDXAP2RBr'
mysql_database = 'devCrcDb'

'''
Connect to database 
'''

cnx = mysql.connector.connect(
    host = mysql_host ,
    port= mysql_port,
    user =  mysql_user ,
    password = mysql_password ,
    database = mysql_database
)



############################################### From EC2

# workingDirectory = os.getcwd()

# parser = configparser.ConfigParser()
# parser.read(os.path.join( workingDirectory ,"config/db.conf"))
# mysql_host = parser.get("db_config", "sql_hostname") 
# mysql_user =  parser.get("db_config", "sql_username") 
# mysql_password = parser.get("db_config", "sql_password") 
# mysql_database = parser.get("db_config", "sql_main_database")


################## load data from parquet file, that contains all the ips
from fastparquet import ParquetFile 
pf = ParquetFile("G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.parquet")
au_ips=pf.to_pandas()

au_ips['Country']='AU'
au_ips.head()

import ipaddress
# int(ipaddress.ip_address('1.2.3.4'))
# str(ipaddress.ip_address(16909060))
# test = au_ips.head()

au_ips['IPAddress_int']=au_ips['IPAddress'].apply(lambda x: int(ipaddress.ip_address(x)))
# int(ipaddress.ip_address(au_ips['IPAddress']))

au_ips = au_ips.drop('IPAddress', axis=1)
columns_titles = ["IPAddress_int","Country"]
au_ips=au_ips.reindex(columns=columns_titles)

############################################### Query
#create the table
cursor = cnx.cursor()
cursor.execute("CREATE TABLE au_ips (IPAddress_int INT UNSIGNED, Country VARCHAR(2))")

# cursor.execute("INSERT INTO au_ips_test VALUES (INET_ATON(%s), 'au')", data_salary)

from sqlalchemy import create_engine
######con
# Set database credentials.
creds = {'usr': mysql_user,
          'pwd': mysql_password,
          'hst': mysql_host,
          'prt': mysql_port,
          'dbn': mysql_database}
# MySQL conection string.
connstr = 'mysql+mysqlconnector://{usr}:{pwd}@{hst}:{prt}/{dbn}'
# Create sqlalchemy engine for MySQL connection.
engine = create_engine(connstr.format(**creds))

# Load data
# au_ips.head(1000000).to_sql(name='au_ips', con=engine, if_exists = 'append', index=False, chunksize=10000)
au_ips.to_sql(name='au_ips', con=engine, if_exists = 'append', index=False, chunksize=100000)

# query to select one IP
# SELECT *, INET_NTOA(IPAddress_int) as IP
# FROM devCrcDb.au_ips
# WHERE INET_ATON('192.168.0.10')=IPAddress_int
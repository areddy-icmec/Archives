import mysql.connector
import configparser
import os
import pandas as pd
from sqlalchemy import create_engine

############################################### Local

mysql_host = 'localhost'
mysql_port='8157'
mysql_user = 'devCrcDbAdmin'
mysql_password = 'sjigjRiQfHVfDXAP2RBr'
mysql_database = 'devCrcDb'

'''
Connect to database 
'''

############################################### From EC2

# workingDirectory = os.getcwd()

# parser = configparser.ConfigParser()
# parser.read(os.path.join( workingDirectory ,"config/db.conf"))
# mysql_host = parser.get("db_config", "sql_hostname") 
# mysql_user =  parser.get("db_config", "sql_username") 
# mysql_password = parser.get("db_config", "sql_password") 
# mysql_database = parser.get("db_config", "sql_main_database")

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

############AU similar match
#read the file with the slangs
au_words=pd.read_excel("G:\My Drive\Project CRC\data\Australian Indicators.xlsx", sheet_name="Australian slang")
# au_words=pd.read_excel("/home/ubuntu/project_crc/webApp/sampleData/Australian Indicators.xlsx", sheet_name="Australian slang")
#slangs
au_words_list = au_words["Slang terms"]
au_words_list=pd.DataFrame(au_words_list)
au_words_list.columns=['word']
au_words_list['source']='slang'

#locations
au_locations=pd.read_excel("G:\My Drive\Project CRC\data\Australian Indicators.xlsx", sheet_name="Australian place names")
# au_locations=pd.read_excel("/home/ubuntu/project_crc/webApp/sampleData/Australian Indicators.xlsx", sheet_name="Australian place names")
au_locations=au_locations.melt(var_name='letter', value_name='word')
au_locations=au_locations.dropna()
au_locations['source']='location'
#append
au_words_all=au_words_list[['word', 'source']]._append(au_locations[['word', 'source']])
# test=pd.DataFrame(au_words_list)
# all_au_words = pd.DataFrame(au_words_list, columns=['au_words'])

au_words_all.to_sql(name='au_words', con=engine, if_exists = 'replace', index=False, chunksize=20000)



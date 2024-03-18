import pandas as pd
import psycopg2
import configparser
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import glob
import os 

parser = configparser.ConfigParser()
parser.read("pipeline.conf")
dbname = parser.get("postgres_config", "database")
user = parser.get("postgres_config", "username")
password = parser.get("postgres_config",
    "password")
host = parser.get("postgres_config", "host")
port = parser.get("postgres_config", "port")

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
Session = sessionmaker(bind=engine)


with Session() as session:
    for each_file in glob.glob(r'/Users/icmec/Documents/censusData/2021_GCP_POA_for_NSW_short-header/2021 Census GCP Postal Areas for NSW/*.csv'):
        df = pd.read_csv(each_file)
        df.replace('..',0, inplace=True)
        fileName = os.path.basename(each_file)
        nameOfDb , _ = os.path.splitext( fileName )
        dtypes = { each_column : sqlalchemy.types.Integer() for each_column in df.columns[1:] }  
        df.to_sql(nameOfDb, con=engine, schema = 'censusNswInit' , if_exists='replace',index=False , dtype=dtypes)
        os.remove(each_file)
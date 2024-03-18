import configparser
from curses import flash
import sqlalchemy
from sqlalchemy import create_engine, false
from sqlalchemy.orm import sessionmaker
import os 
import glob
import pandas as pd


def GetConfiguration():
    details = {}
    parser = configparser.ConfigParser()
    current_directory =  os.getcwd()
    parser.read(f"{current_directory}/conf/postgres.conf")
    details['dbname'] = parser.get("postgres_config", "database")
    details['user'] = parser.get("postgres_config", "username")
    details['password'] = parser.get("postgres_config","password")
    details['host'] = parser.get("postgres_config", "host")
    details['port'] = parser.get("postgres_config", "port")
    return details



def SendData(df,table_name , index = 'False', schema_name = 'stage' ,if_exists_flag = 'append'):
    postgresConfig = GetConfiguration()
    engine = create_engine(f'postgresql://{postgresConfig["user"]}:{postgresConfig["password"]}@{postgresConfig["host"]}:{postgresConfig["port"]}/{postgresConfig["dbname"]}')
    Session = sessionmaker(bind=engine)
    with Session() as session:
        df.to_sql(table_name, con=engine, schema = schema_name , if_exists=if_exists_flag,index=index )
    return 'success'

def GetData(sql):
    postgresConfig = GetConfiguration()
    engine = create_engine(f'postgresql://{postgresConfig["user"]}:{postgresConfig["password"]}@{postgresConfig["host"]}:{postgresConfig["port"]}/{postgresConfig["dbname"]}')
    Session = sessionmaker(bind=engine)
    with Session() as session:
       df =  pd.read_sql(sql, con=engine)
    return  df

def ExtractTables(path_to_folder,join_on ):
    listOfDf = []
    
    for each in glob.glob(f'{path_to_folder}/*.csv'):
        df = pd.read_csv(each)
        fileName = os.path.basename(each)
        _,requiredId,_,_ = fileName.split('_')
        renamedColnames = [join_on.lower()] #since columns from two or more tables have same columnname 
        renamedColnames.extend( [ f'{requiredId.lower()}.{each.lower()}' for each in df.columns[1:]]  )
        df.columns = renamedColnames
        listOfDf.append(df)
    
    merged = listOfDf[0]
    for df in listOfDf[1:]:
        merged = pd.merge(merged, df, how='inner' , on=join_on.lower())

    return merged


def Test():
    print('Hellp')

# def make_connection():
#     postgresConfig = GetConfiguration()
#     engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
#     Session = sessionmaker(bind=engine)
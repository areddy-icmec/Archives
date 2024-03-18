import configparser
import sqlalchemy
from sqlalchemy import create_engine, false
from sqlalchemy.orm import sessionmaker


def GetConfiguration():
    details = {}
    parser = configparser.ConfigParser()
    parser.read("/Users/icmec/Documents/CONFIGURATIONS/postgres.conf")
    details['dbname'] = parser.get("postgres_config", "database")
    details['user'] = parser.get("postgres_config", "username")
    details['password'] = parser.get("postgres_config","password")
    details['host'] = parser.get("postgres_config", "host")
    details['port'] = parser.get("postgres_config", "port")
    return details

def TestFunc():
    print('Hello')

def SendData(df,table_name , schema_name = 'stage' ,if_exists_flag = 'append'):
    postgresConfig = GetConfiguration()
    engine = create_engine(f'postgresql://{postgresConfig["user"]}:{postgresConfig["password"]}@{postgresConfig["host"]}:{postgresConfig["port"]}/{postgresConfig["dbname"]}')
    Session = sessionmaker(bind=engine)
    with Session() as session:
        df.to_sql(table_name, con=engine, schema = schema_name , if_exists=if_exists_flag,index=False )
    return 'success'

def TestFunc2():
    print('Hello')


# def make_connection():
#     postgresConfig = GetConfiguration()
#     engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
#     Session = sessionmaker(bind=engine)
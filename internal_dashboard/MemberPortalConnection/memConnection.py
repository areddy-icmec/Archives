import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import sshtunnel as sshtunnel
import logging
import configparser
import os 
import datetime
import pickle
import json




date_time = datetime.datetime.now()

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s" 
logging.basicConfig( filename='logger.log' ,  level= logging.INFO , format= LOG_FORMAT  )
logger = logging.getLogger()


#Change this to the private key in local 
mypkey = paramiko.Ed25519Key.from_private_key_file('/Users/icmec/.ssh/wpengine_icmec27012023')


parser = configparser.ConfigParser()
current_directory =  os.getcwd()
parser.read(f"{current_directory}/conf/db.conf")

sql_hostname = parser.get("db_config", "sql_hostname") 
sql_username =  parser.get("db_config", "sql_username") 
sql_password = parser.get("db_config", "sql_password")
sql_main_database = parser.get("db_config", "sql_main_database")
sql_port = parser.getint("db_config", "sql_port")
ssh_host = parser.get("db_config", "ssh_host")
ssh_user = parser.get("db_config", "ssh_user")
ssh_port = parser.getint("db_config", "ssh_port")

global resultJson; resultJson = {};
#resultJson['Date'] = date_time.strftime("%d/%m/%Y")

def getNumberOfMembers(con):
   query = '''SELECT CAST(`user_registered` AS DATE) AS date ,COUNT(*) AS cnt FROM `wp_users` WHERE user_login != 'wpengine' GROUP BY CAST(`user_registered` AS DATE)'''
   membersDf =  pd.read_sql_query(query, con)
   membersDf['cumulative'] = membersDf['cnt'].cumsum()
   membersDf = membersDf.set_index('date')
   resultJson['numMembers'] = membersDf.to_dict()

def getNumberOfMessage(con):
   query = '''SELECT CAST(`date_sent` AS DATE) AS date,COUNT(*) as cnt FROM `wp_bp_messages_messages` GROUP BY CAST(`date_sent` AS DATE)'''
   messagesDf =  pd.read_sql_query(query, con)
   messagesDf['cumulative'] = messagesDf['cnt'].cumsum()
   messagesDf = messagesDf.set_index('date')
   resultJson['numMessages'] = messagesDf.to_dict()

def getNumberOfInvitations(con):
   query = '''SELECT CAST(`date_modified` AS DATE) AS date,COUNT(*) as cnt FROM `wp_bp_invitations` GROUP BY CAST(`date_modified` AS DATE)'''
   invitationsDf =  pd.read_sql_query(query, con)
   invitationsDf['cumulative'] = invitationsDf['cnt'].cumsum()
   invitationsDf = invitationsDf.set_index('date')
   resultJson['numInvitations'] = invitationsDf.to_dict()

def getNumberOfConnections(con):
   query = '''SELECT CAST(`date_created` AS DATE) AS date,COUNT(*) as cnt FROM `wp_bp_friends` GROUP BY CAST(`date_created` AS DATE)'''
   connectionsDf =  pd.read_sql_query(query, con)
   connectionsDf['cumulative'] = connectionsDf['cnt'].cumsum()
   connectionsDf = connectionsDf.set_index('date')
   resultJson['numConnections'] = connectionsDf.to_dict()

def getPosts(con):
   query = '''SELECT CAST(`post_date` AS DATE) AS date,COUNT(*) as post,SUM(comment_count) as comments  FROM `wp_posts` where post_type = 'tribe_events' GROUP BY CAST(`post_date` AS DATE)'''
   postsDf =  pd.read_sql_query(query, con)
   postsDf['cumulative'] = postsDf['post'].cumsum()
   postsDf = postsDf.set_index('date')
   resultJson['Posts'] = postsDf.to_dict()

def getEvents(con):
   query = '''SELECT CAST(`post_date` AS DATE) AS date,COUNT(*) as event,SUM(comment_count) as comments  FROM `wp_posts` where post_type = 'tribe_events' GROUP BY CAST(`post_date` AS DATE)'''
   eventsDf =  pd.read_sql_query(query, con)
   eventsDf['cumulative'] = eventsDf['event'].cumsum()
   eventsDf = eventsDf.set_index('date')
   resultJson['Events'] = eventsDf.to_dict()

def getProfileUpdaters(con):
   query = '''SELECT CAST(wp_bp_activity.date_recorded AS DATE)  AS date , wp_users.display_name as name,wp_bp_activity.type FROM `wp_bp_activity`  LEFT JOIN `wp_users` on wp_bp_activity.user_id = wp_users.ID WHERE type = \'updated_profile\''''
   UpdatersDf =  pd.read_sql_query(query, con)
   #eventsDf['cumulative'] = eventsDf['event'].cumsum()
   #UpdatersDf = UpdatersDf.set_index('date')
   resultJson['Updaters'] = UpdatersDf.to_dict()
   print(resultJson['Updaters'])




#save the result
def pickleSave():
    #name =  date_time.strftime("%d%m%Y")
    with open('data/portalData'+ '.pickle', 'wb') as handle:
        pickle.dump(resultJson, handle, protocol=pickle.HIGHEST_PROTOCOL)


try:
        with SSHTunnelForwarder( (ssh_host,ssh_port),ssh_username=ssh_user,ssh_pkey=mypkey,remote_bind_address=(sql_hostname, sql_port) ) as tunnel:
                
                #establish  connection to the member portal via pymysql
                conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                passwd=sql_password, db=sql_main_database,
                port=tunnel.local_bind_port)
                print('here')
                cur = conn.cursor()
                getNumberOfMembers(conn)
                getNumberOfMessage(conn)
                getNumberOfInvitations(conn)
                getNumberOfConnections(conn)
                getPosts(conn)
                getEvents(conn)
                getProfileUpdaters(conn)

                conn.close()
                logger.info('Successfully extracted information')
                
except Exception as e:
        conn.close()
        logger.error(e)

pickleSave()
#Diagram
from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.aws.database import RDSMysqlInstance
from diagrams.aws.compute import Lambda
from diagrams.aws.compute import EC2
from diagrams.aws.migration import TransferForSftp
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import User
from diagrams.aws.storage import SimpleStorageServiceS3Object
from diagrams.aws.security import Cognito
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.network import ALB 


import os
# Change the current working directory
os.chdir('G:/My Drive/Project Lighthouse/project_lighthouse/')

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

## this Architecture diagram was to showcase the arhcitecture to the aws team, this architecture is expected to change in overtime.
#Furthur Action 
#1. Make the project work insensitive to folder path use os.getcwd() and os.path.join( os.getcwd() , 'data' ) 

workingDirectory = os.getcwd()
print(workingDirectory)

with Diagram("Projectv4",  filename= os.path.join( workingDirectory , "architecture/results/architecture-current" ) , show=True):
    
    with Cluster("External Data", direction="LR"):
        with Cluster("CRC",direction="LR"):
            csv_file1 = Custom("blacklist", os.path.join( workingDirectory , "architecture/customImages/csv.png" ) )
            csv_file2 = Custom("chat", os.path.join( workingDirectory , "architecture/customImages/csv.png" ))
            csv_file3 = Custom("p2p", os.path.join( workingDirectory , "architecture/customImages/csv.png" ))
            csv_group=[csv_file1, csv_file2, csv_file3]
            
        with Cluster("ATII",direction="LR"):
            csv_file4 = Custom("Crypto", os.path.join( workingDirectory , "architecture/customImages/csv.png" ) )
            csv_group2=[csv_file4]
            
        with Cluster("GeoGuard",direction="LR"):
            mmdb_file = SimpleStorageServiceS3Object("MMDB")
            csv_file5 = Custom("Geo", os.path.join( workingDirectory , "architecture/customImages/csv.png" ) )
            group3=[csv_file5, mmdb_file]
           
    with Cluster("Amazon Web Services",direction="LR"):
   
        with Cluster("ETL",direction="LR"):
            with Cluster("Extract",direction="LR"):
               sftp = TransferForSftp( 'File Transfer')
               landS3 =  S3("Landing Zone")
               sftp >> landS3
               csv_group2 >> landS3 
               csv_group >> sftp 
               lamda_api = Lambda("API")
               group3 >> lamda_api
               lamda_api >> landS3 
            with Cluster("Transform",direction="LR"):
               lamda_trans_crc = Lambda("Transform CRC")
               lamda_trans_crypto = Lambda("Transform Crypto")
               lamda_trans_geo = Lambda("Transform Geo")
               transferS3 =  S3("Transform Zone")
               landS3 >> lamda_trans_crc >> transferS3
               landS3 >> lamda_trans_crypto >> transferS3
               landS3 >> lamda_trans_geo >> transferS3
            with Cluster("Load",direction="LR"):
               lamda_load_crc = Lambda("Load CRC")
               lamda_load_crypto = Lambda("Load Crypto")
               lamda_load_geo = Lambda("Load Geo")
               RDS=RDSPostgresqlInstance("PostgreSQL Database")
               transferS3 >> lamda_load_crc >> RDS
               transferS3 >> lamda_load_crypto >> RDS
               transferS3 >> lamda_load_geo >> RDS
    
        
        # with Cluster('Analytics'):
        #     lamda_Analytics = Lambda("Jaro Winkler dist")
        #     ddb = Dynamodb("Dynamo Db")
        #     lamda_Analytics >> ddb
    
        # transferS3 >>  lamda_Analytics

        with Cluster('Development Enviroment'):
            ec2_dev = EC2("EC2 Development \n Streamlit Web App")
            # streamlit_dev = Custom("Streamlit", os.path.join( workingDirectory , "architecture/customImages/streamlit.png" ) )
        
        # with Cluster('Production Enviroment'):
        #     ec2_prod = EC2("VM Production")
        #     streamlit_prod = Custom("Streamlit", os.path.join( workingDirectory , "architecture/customImages/streamlit.png" ) )
        #     application_load_balancer = ALB("Application Load Balancer")
        #     auth = Cognito("Authentication")
        
    with Cluster("Internal (intranet)", direction="LR"):
        tester_user = User("Developer/Tester")
    
    with Cluster("External API (internet)", direction="LR"):
        api_geoguard = Custom("GeoGuard", os.path.join( workingDirectory , "architecture/customImages/api.png" ) )
        api_ip2location= Custom("IP2Location", os.path.join( workingDirectory , "architecture/customImages/api.png" ) )
        api_group=[api_geoguard, api_ip2location]
    # with Cluster("External (internet)", direction="LR"):
    #     final_user = User("Final User")


    #dev
    RDS - ec2_dev
    # api_geoguard >> ec2_dev
    # api_geoguard << ec2_dev
    # api_ip2location >> ec2_dev
    # api_ip2location << ec2_dev
    api_group - ec2_dev
    # api_group << ec2_dev
    ec2_dev - tester_user
    # ec2_dev << tester_user

    # #prod
    # RDS >> ec2_prod
    # api_group >> ec2_prod
    # api_group << ec2_prod
    # ec2_prod >> streamlit_prod
    # ec2_prod << streamlit_prod
    # streamlit_prod << application_load_balancer
    # streamlit_prod >> application_load_balancer
    # application_load_balancer >> auth
    # application_load_balancer << auth
    # auth >> final_user
    # auth << final_user
    

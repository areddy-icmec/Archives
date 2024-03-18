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

with Diagram("Projectv3",  filename= os.path.join( workingDirectory , "architecture/results/archi" ) , show=False):
       
    with Cluster("ETL",direction="LR"):
       sftp = TransferForSftp( 'File Transfer' )
       landS3 =  S3("Landing Zone")
       sftp >> landS3

       lamda_api = Lambda("API")
       lamda_trans = Lambda("Transform")
       transferS3 =  S3("Transform Zone")
       landS3 >> lamda_trans >> transferS3
   
       lamda_load = Lambda("Load")
       RDS=RDSPostgresqlInstance("PostgreSQL Database")
       lamda_load >> RDS
       transferS3 >>  lamda_load
    
    with Cluster("Data", direction="LR"):
        with Cluster("CRC",direction="LR"):
            csv_file1 = Custom("blacklist", os.path.join( workingDirectory , "architecture/customImages/csv.png" ) )
            csv_file2 = Custom("chat", os.path.join( workingDirectory , "architecture/customImages/csv.png" ))
            csv_file3 = Custom("p2p", os.path.join( workingDirectory , "architecture/customImages/csv.png" ))
            csv_group=[csv_file1, csv_file2, csv_file3]
            csv_group >> sftp 
            
        with Cluster("ATII",direction="LR"):
            csv_file4 = Custom("Crypto", os.path.join( workingDirectory , "architecture/customImages/csv.png" ) )
            csv_group2=[csv_file4]
            csv_group2 >> landS3 
            
        with Cluster("GeoGuard",direction="LR"):
            mmdb_file = SimpleStorageServiceS3Object("MMDB")
            csv_file5 = Custom("Geo", os.path.join( workingDirectory , "architecture/customImages/csv.png" ) )
            group3=[csv_file5, mmdb_file]
            group3 >> lamda_api
            lamda_api >> landS3 
            
   
    
    # with Cluster('Analytics'):
    #     lamda_Analytics = Lambda("Jaro Winkler dist")
    #     ddb = Dynamodb("Dynamo Db")
    #     lamda_Analytics >> ddb

    # transferS3 >>  lamda_Analytics
    with Cluster('Development Enviroment'):
        ec2_dev = EC2("VM Development")
        streamlit_dev = Custom("Streamlit", os.path.join( workingDirectory , "architecture/customImages/streamlit.png" ) )
        tester_user = User("Developer/Tester")
    
    with Cluster('Production Enviroment'):
        ec2_prod = EC2("VM Production")
        streamlit_prod = Custom("Streamlit", os.path.join( workingDirectory , "architecture/customImages/streamlit.png" ) )
        auth = Cognito("Authentication")
        final_user = User("Final User")

    #dev
    RDS >> ec2_dev
    ec2_dev >> streamlit_dev
    ec2_dev << streamlit_dev
    streamlit_dev >> tester_user
    streamlit_dev << tester_user

    
    #prod
    RDS >> ec2_prod
    ec2_prod >> streamlit_prod
    ec2_prod << streamlit_prod
    streamlit_prod >> auth
    streamlit_prod << auth
    auth >> final_user
    auth << final_user
    
    
  #################################Add a layer as 'dev env' and 'prod env'



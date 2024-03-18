#Diagram
from diagrams import Cluster, Diagram, Edge
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

with Diagram("Projectv4",  filename= os.path.join( workingDirectory , "databaseArchitecture/results/databasearchitecture" ) , show=True, direction="LR"):
    with Cluster("ATII", direction="LR"):
        atii_tbl = Custom("atii_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        crypto_tbl = Custom("crypto_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        darknet_url_tbl = Custom("darknet_url_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )

    atii_tbl - Edge(label="crypto_address") - crypto_tbl
    
    with Cluster("GeoComply", direction="LR"):
        geoguard_anonymizers_tbl = Custom("geoguard_anonymizers_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        geoguard_geoip_tbl = Custom("geoguard_geoip_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        geoguard_group=[geoguard_anonymizers_tbl, geoguard_geoip_tbl]

    geoguard_anonymizers_tbl - Edge(label="created_at \n network") - geoguard_geoip_tbl

    with Cluster("CRC (Main)", direction="LR"):
        crc_data_tbl = Custom("crc_data_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        crc_geoguard_tbl = Custom("crc_geoguard_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        crc_geoip_outliers_tbl = Custom("crc_geoip_outliers_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        crc_geoip_tbl = Custom("crc_geoip_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        with Cluster("Blacklist", direction="LR"):
            ips_blacklist_tbl = Custom("ips_blacklist_tbl", os.path.join( workingDirectory , "databaseArchitecture/customImages/table-icon.png" ) )
        # crc_data_and_geo=[crc_data_tbl, crc_geoguard_tbl, crc_geoip_outliers_tbl, crc_geoip_tbl]
    
            
    
        crc_data_tbl - crc_geoguard_tbl
        crc_data_tbl - crc_geoip_outliers_tbl
        crc_data_tbl - crc_geoip_tbl
        crc_data_tbl - ips_blacklist_tbl
        crc_geoguard_tbl - crc_geoip_outliers_tbl
        crc_geoip_outliers_tbl - crc_geoip_tbl
        # crc_geoguard_tbl - crc_geoip_tbl

    # crc_data_and_geo >> crc_data_and_geo
    # geoguard_group - Edge(label="timestamp_utc \n ip_address") - crc_data_and_geo
    
    # crc_data_tbl - Edge(label="timestamp_utc \n ip_address") - crc_geoguard_tbl
    # # crc_data_tbl - Edge(label="timestamp_utc \n ip_address (network)") - geoguard_geoip_tbl
    # crc_data_tbl - Edge(label="timestamp_utc \n ip_address (network)") - geoguard_group
    # crc_geoip_outliers_tbl - Edge(label="timestamp_utc \n ip_address (network)") - geoguard_group

    # geoguard_group
    # crc_data_tbl - Edge(label="timestamp_utc \n ip_address (network)") - geoguard_anonymizers_tbl


    


    # #dev
    # RDS - ec2_dev
    # # RDS << ec2_dev
    # api_group - Edge(color="blue") - ec2_dev
    # # ec2_dev - Edge(color="blue") - tester_user
    # ec2_dev - tester_user

    # # ec2_dev << tester_user
    # # ec2_dev << application_load_balancer
    # # ec2_dev >> application_load_balancer
    

    # #prod
    # RDS - ec2_prod
    # # RDS << ec2_prod
    # api_group - Edge(color="dark_blue") - ec2_prod
    # # api_group << ec2_prod
    # ec2_prod - application_load_balancer
    # # ec2_prod >> application_load_balancer
    # # application_load_balancer >> auth
    # application_load_balancer - auth
    # auth - final_user
    # ec2_prod >> final_user

    

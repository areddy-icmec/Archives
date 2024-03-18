#Diagram
from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.aws.database import RDSMysqlInstance
from diagrams.aws.compute import Lambda
from diagrams.aws.compute import EC2


with Diagram("Project CRC", show=False):
    
    streamlit = Custom("streamlit", "streamlit.png")
      
    with Cluster("CRC Data"):
        csv_file1 = Custom("blacklist", "csv.png")
        csv_file2 = Custom("chat", "csv.png")
        csv_file3 = Custom("p2p", "csv.png")
        csv_group=[csv_file1, csv_file2, csv_file3]
        
    with Cluster("Website Transactions"):
        lamda_load = Lambda("Load")
        RDS=RDSMysqlInstance("MySQL")
        lamda_load >> RDS
        
    with Cluster("Analytics"):
        ec2_trans = EC2("VM")
        S3_store2=S3("S3 bucket output")
        ec2_trans >> S3_store2
    
    lamda_trans=Lambda("Transform")
    S3_store=S3("S3 bucket storage")
    streamlit
    
    csv_group >> lamda_trans >> S3_store>> lamda_load # >> RDS >> ec2_trans >> streamlit
    RDS >> streamlit
    RDS << streamlit
    S3_store >> ec2_trans
    S3_store2 >> streamlit

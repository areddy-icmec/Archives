from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
import os 

'''
Need a pyspark environment to run this script.
'''
workingDirectory = os.getcwd()

spark = SparkSession.builder.master("local[*]").getOrCreate()

chatDf = spark.read.csv(os.path.join( workingDirectory , "sampleData/crc_ips_observed_chat__yyyy-mm-dd_.csv" ) , header=True, inferSchema=True)

chatDf = chatDf.withColumn( 'chat' , lit(1) )

p2pDf = spark.read.csv(os.path.join(workingDirectory,"sampleData/crc_ips_observed_p2p__yyyy-mm-dd_.csv") , header=True, inferSchema=True)

ipBlacklistDf = spark.read.csv(os.path.join(workingDirectory,"sampleData/crc_ips_blacklist__yyyy-mm-dd_.csv"), header=True, inferSchema=True)

chatDf.printSchema()
p2pDf.printSchema()
ipBlacklistDf.printSchema()

merged_df = chatDf.unionByName(p2pDf, allowMissingColumns=True)
merged_df.show(2)


merged_df = merged_df.join(ipBlacklistDf,merged_df.IPAddress ==  ipBlacklistDf.IPAddress,"left").drop(ipBlacklistDf.IPAddress).show(truncate=False)
merged_df.printSchema()

merged_df = merged_df.coalesce(1)

merged_df.write.option("header",True).csv("merged")


'''convert dataframe to parquet format and save it in hive partitioned table'''
# merged_df.write.parquet("merged", mode="overwrite", partitionBy=["chat"])




import pandas as pd

au_ip=pd.read_excel("G:\My Drive\Project CRC\data\Australian Registered IP Addresses.xlsx", skipfooter=2)
# au_ip

import ipaddress
# au_ip['Begin IP Address'][0]
# au_ip['End IP Address'][0]

range_of_ips=list()

for i in range(0,len(au_ip)):
# for i in range(0,10):

    print(i)
    start_ip = ipaddress.IPv4Address(au_ip['Begin IP Address'][i])
    end_ip = ipaddress.IPv4Address(au_ip['End IP Address'][i])

    for ip_int in range(int(start_ip), int(end_ip)+1):
        aux=ipaddress.IPv4Address(ip_int)
        # print(aux)
        range_of_ips.append(aux.compressed)

# range_of_ips
df_ip=pd.DataFrame(range_of_ips)
df_ip.columns=['IPAddress']

from fastparquet import write
write("G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.parquet", df_ip, compression='GZIP')

# df_ip.to_csv("G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.csv", index=False)

# df_ip.to_parquet("G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.parquet", compression=None)

# import pyarrow as pa    
# table = pa.Table.from_pandas(df_ip)

# import pyarrow.parquet as pq
# pq.write_table(table, "G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.parquet")

from fastparquet import ParquetFile 
pf = ParquetFile("G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.parquet")
au_ips=pf.to_pandas()
# au_ips
# au_ips=pd.read_csv("G:\My Drive\Project CRC\data\Australian Registered IP Addresses Long.csv", engine="pyarrow")

df1=pd.read_csv(r'G:\My Drive\Project CRC\data\crc_ips_observed_p2p__yyyy-mm-dd_.csv') 
df2=pd.read_csv(r'G:\My Drive\Project CRC\data\crc_ips_observed_chat__yyyy-mm-dd_.csv') 

#clean
df1=df1.dropna(axis=0, how='all')
df=df1.filter(items=['UserName',"Timestamp", "IPAddress", "Country", "Region", "ISP", "Org"])
df2=df2.filter(items=['UserName',"Timestamp", "IPAddress", "Country", "Region", "ISP", "Org"])
df=df.append(df2)

#join
merged_ips=df.merge(au_ips, on='IPAddress')

merged_ips['Country']='AU'

merged_ips.to_csv("G:\My Drive\Project CRC\data\Australian CRC IPs.csv", encoding='utf-8', index=False)


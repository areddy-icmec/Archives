###Create the Api key
#go to https://console.cloud.google.com/projectselector2/apis/credentials?_ga=2.114327630.858015989.1663548417-535358721.1663293786&supportedpurview=project
#API->Credentials->create new service account
#I created one called : ga4-etl@icmec-au-ga-python-etl.iam.gserviceaccount.com
#Go to the service->Keys->use the key -> 6608a68cbb8b084e7e02a159f2ddedad1cae94b8

#follow this video
#https://www.youtube.com/watch?v=VP09MqtstSE
#or this video
#https://www.youtube.com/watch?v=Uk28ec4W4sA

#install in the enviroment 
#pip install git+https://github.com/DataSolveProblems/jj_data_connector.git

import pandas as pd
import os
from jj_data_connector.ga4 import  GA4RealTimeReport,GA4Report, Metrics, Dimensions

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'conf/googleAnalyticsKey.json'
#Fund property ID
property_id = '325695411'

#1st type of reports: Realtime
#API schema
#https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-api-schema 

dims=['city','minutesAgo']
metrics=['activeUsers']

ga4_realtime=GA4RealTimeReport(property_id)
response=ga4_realtime.query_report(dims, metrics)
print(response)

df=pd.DataFrame(data=response['rows'], columns=response['headers'])

#2nd type of reports: Historic

# creating GA4Report object instance
#API Schema
#https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
ga4 = GA4Report(property_id)

print(Metrics)
print(Dimensions)

# variables
dimension_list = ['date', 'city','cityId']
metric_list = ['newUsers','totalUsers', 'bounceRate']
#date_range = ('2022-09-01', '2022-09-20')
date_range = ('2022-01-01', 'today')

# run the GA4 report
report = ga4.run_report(
    dimension_list, 
    metric_list, 
    date_ranges=[date_range],
    row_limit=100000,
    offset_row=0
)

report['row_count']

# report.keys()
print(report['response'])

report['headers']
report['rows']
df = pd.DataFrame(columns=report['headers'], data=report['rows'])
print(df)


dire='files/'

# export to Excel files
df.to_excel(dire+'cities_users.xlsx', index=False)

#new report with countries per week
# variables
dimension_list = ['date', 'country']
metric_list = ['newUsers','totalUsers', 'screenPageViews']
#date_range = ('2022-09-01', '2022-09-20')
date_range = ('2022-01-01', 'today')

# run the GA4 report
report = ga4.run_report(
    dimension_list, 
    metric_list, 
    date_ranges=[date_range],
    row_limit=100000,
    offset_row=0
)

report['row_count']

# report.keys()
print(report['response'])

report['headers']
report['rows']
df = pd.DataFrame(columns=report['headers'], data=report['rows'])
print(df)

# export to Excel files  
df.to_excel(dire+'countries_users.xlsx', index=False)

####group by AU vs rest of the world, write as 'activity_type'
grouped_data=df.copy()
grouped_data.info()
grouped_data=grouped_data.apply(lambda col:pd.to_numeric(col, errors='coerce'))
grouped_data['country']=df['country']
grouped_data=grouped_data.groupby(['country','date']).sum()
grouped_data=grouped_data.reset_index()
activity_type=grouped_data.copy()
import numpy as np
activity_type['activity_type'] = np.where(grouped_data['country'] == 'Australia', 'au', 'row')
activity_type_grouped=activity_type.groupby(['activity_type','date']).sum()
activity_type_grouped=activity_type_grouped.reset_index()
activity_type_melted=pd.melt(activity_type_grouped, id_vars=['activity_type','date'])
resulting_df=activity_type_melted.copy()
resulting_df['activity_type']=resulting_df['variable']+'_'+resulting_df['activity_type']
resulting_df = resulting_df.drop('variable', axis=1)
resulting_df['date']=pd.to_datetime(resulting_df['date'], format='%Y%m%d')
resulting_df['app']='Google Analytics'

# export to Excel files
resulting_df.to_excel(dire+'countries_users_activity_type.xlsx', index=False)

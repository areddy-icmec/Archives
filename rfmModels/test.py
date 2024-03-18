import pandas as pd
import os
import datetime as dt
# from helpers.queries import *
import streamlit.components.v1 as components
from IPython.core.display import display, HTML
import streamlit as st
# from helpers.password import *
import plotly.graph_objects as go
from scipy import stats


directory="G:/My Drive/Project Lighthouse/project_lighthouse/webApp/helpers/queries.py"

# #ec2
# directory="/home/ubuntu/project_crc/webApp/queries.py"

with open(directory) as infile:
    exec(infile.read())
    
selected_time_range_ini=pd.to_datetime('07-01-2022 00:00')
selected_time_range_end=pd.to_datetime('08-01-2022 23:59')

########### create a rfm model using crc data
#get the data
mydata=crc_between_datetimes(selected_time_range_ini,selected_time_range_end)
#print the number of rows
print(mydata.shape)
# mydata=mydata.head(1000)

#select only 'timestamp_utc','ip_address'
mydata=mydata[['timestamp_utc','ip_address']]
#order by ip_address and timestamp_utc
mydata=mydata.sort_values(by=['ip_address','timestamp_utc'])
# "timestamp_utc", "ip_address", "user_id", "user_name", "country", "isp", "vendor", "channel",
print(mydata)
#####features
#calculate the number of times it appears
features=mydata.groupby('ip_address').size().reset_index(name='counts')
print(features)
#calculate the last 'timestamp_utc' it appeared since today
# features['last_time_utc']=mydata.groupby('ip_address')['timestamp_utc'].max()
last_date_appeared=mydata.sort_values(by=['timestamp_utc']).drop_duplicates(subset='ip_address', keep='last')
#calculate the number of days since today
last_date_appeared['days_since_today']=last_date_appeared['timestamp_utc'].apply(lambda x: (dt.datetime.now() - x).days)    
print(last_date_appeared)
#merge features with last_date_appeared
features=features.merge(last_date_appeared, on='ip_address', how='left')
print(features)
#drop the timestamp_utc column
features=features.drop(['timestamp_utc'], axis=1)
#plot the features in a scatterplot using matplotlib
import matplotlib.pyplot as plt
plt.scatter(features['counts'], features['days_since_today'])

# #graph the features
# import seaborn as sns #Data visualization
# import matplotlib.pyplot as plt #Data visualization 
# sns.FacetGrid(features).map(plt.scatter,'counts','days_since_today').add_legend()

#####build a cluster using pycaret

# import pycaret as pc
#https://github.com/psrana/Machine-Learning-using-PyCaret/blob/main/03_PyCaret_for_Clustering_with_Results.ipynb
from pycaret.clustering import *
data=features
#drop ip_address column
data=data.drop(['ip_address'], axis=1)
# data = features.sample(frac=0.95, random_state=786).reset_index(drop=True)
# data_unseen = features.drop(data.index).reset_index(drop=True)

# st.write('Data for Modeling: ' + str(data.shape))
# st.write('Unseen Data For Predictions: ' + str(data_unseen.shape))

exp_clu101 = setup(data, normalize = True, session_id = 123)

# #create a cluster
kmeans = create_model('kmeans')
print(kmeans)
plot_model(kmeans, plot = 'elbow')
kmean_results = assign_model(kmeans)
kmean_results.head()
plot_model(kmeans)
all_metrics = get_metrics()
print(all_metrics)
# # #create a cluster
# kmeans = create_model('kmeans')


#################################################################todo
############################## hacer lo mismo con https://scikit-learn.org/stable/modules/clustering.html


#  ###Per IP
# import plotly.express as px
# # fig = px.bar(isp_total, x="isp", y="counts", orientation='h')
# ips_frequency=crc_ips_frequency_between_datetimes_for_specific_country(selected_time_range_ini, selected_time_range_end, "AU")
# ips_frequency=ips_frequency.sort_values('count', ascending=True)
# fig = px.bar(ips_frequency, x="count",  y="ip_text", orientation='h', color="count")
# st.write("#### Top IP detections")
# st.markdown('The following list show the most wanted offenders in Australia by <abbr title="An Internet Protocol address (IP address) is a numerical label such as 192.0.2.1 that is connected to a computer network that uses the Internet Protocol for communication">IP address</abbr>.', unsafe_allow_html=True)
# st.plotly_chart(fig, use_container_width=True)

# import plotly
# import plotly.express as px
# import chart_studio.plotly as py
# from plotly.offline import plot
# # Visualize the clusters in 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(X.num_priv_msgs, X.num_posts, X.num_img_up)
# ax.set_title('All data')
# ax.set_xlabel('num_priv_msgs')
# ax.set_ylabel('num_posts')
# ax.set_zlabel('num_img_up')
# %matplotlib inline
# plt.show()

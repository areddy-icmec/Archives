import pandas as pd
import os
import datetime as dt
from helpers.queries import *
import streamlit.components.v1 as components
from IPython.core.display import display, HTML
import streamlit as st
from helpers.password import *
import plotly.graph_objects as go
from scipy import stats


# directory="G:/My Drive/Project Lighthouse/project_lighthouse/webApp/helpers/queries.py"

# # #ec2
# # directory="/home/ubuntu/project_crc/webApp/queries.py"

# with open(directory) as infile:
#     exec(infile.read())
    
# df_atii=atii_all_data()

#start of the streamlit page


#logo
workingDirectory = os.getcwd()
col1, col2 = st.columns([4, 5])
with col1:
    st.header('Project Lighthouse')
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/9/9b/Lighthouse_icon.svg', width=50)

#Graphs in new 2 rows 2 col
import pandas as pd
col1, col2 = st.columns(2)
with col1:
        date_initial = st.date_input(
        "Start Date",
        pd.to_datetime('07-01-2022').normalize())
with col2:
    date_end = st.date_input(
    "End Date",
    # pd.to_datetime('today').normalize())
    pd.to_datetime('31-07-2022').normalize())

selected_time_range_ini="{} {}".format(date_initial,'00:00')
selected_time_range_end="{} {}".format(date_end,'23:59')

########### create a rfm model using crc data
#get the data
mydata=crc_between_datetimes(selected_time_range_ini,selected_time_range_end)
mydata=mydata.head(100)
#select only 'timestamp_utc','ip_address'
mydata=mydata[['timestamp_utc','ip_address']]
#order by ip_address and timestamp_utc
mydata=mydata.sort_values(by=['ip_address','timestamp_utc'])
# "timestamp_utc", "ip_address", "user_id", "user_name", "country", "isp", "vendor", "channel",
st.dataframe(mydata, use_container_width=True)

#####features
#calculate the number of times it appears
features=mydata.groupby('ip_address').size().reset_index(name='counts')
st.dataframe(features, use_container_width=True)
#calculate the last 'timestamp_utc' it appeared since today
# features['last_time_utc']=mydata.groupby('ip_address')['timestamp_utc'].max()
last_date_appeared=mydata.sort_values(by=['timestamp_utc']).drop_duplicates(subset='ip_address', keep='last')
#calculate the number of days since today
last_date_appeared['days_since_today']=last_date_appeared['timestamp_utc'].apply(lambda x: (dt.datetime.now() - x).days)    
st.dataframe(last_date_appeared, use_container_width=True)
#merge features with last_date_appeared
features=features.merge(last_date_appeared, on='ip_address', how='left')
st.dataframe(features, use_container_width=True)
#drop the timestamp_utc column
features=features.drop(['timestamp_utc'], axis=1)

#####build a cluster using pycaret

# import pycaret as pc
from pycaret.clustering import *
data=mydata
# data = features.sample(frac=0.95, random_state=786).reset_index(drop=True)
# data_unseen = features.drop(data.index).reset_index(drop=True)

# st.write('Data for Modeling: ' + str(data.shape))
# st.write('Unseen Data For Predictions: ' + str(data_unseen.shape))

exp_clu101 = setup(data, normalize = True, session_id = 123)

# #create a cluster
kmeans = create_model('kmeans')
print(kmeans)
kmean_results = assign_model(kmeans)
kmean_results.head()
plot_model(kmeans)
all_metrics = get_metrics()
st.dataframe(all_metrics, use_container_width=True)

# # #create a cluster
# kmeans = create_model('kmeans')



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

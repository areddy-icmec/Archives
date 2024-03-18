import pandas as pd
import datetime
import numpy as np

#data is imported from PODIO ETL #this should query the DB
#dire='G:\\My Drive\\Podio Reports\\Data\\'
#importing the datatable
activity=pd.read_excel('files/app_activities_dataset.xlsx', 'Sheet1')
activity['created_on']= pd.to_datetime(activity['created_on'])
activity['created_on'] = activity['created_on'].dt.date
#cleaning #I'm filtering out the last closing probability because is a number
len(activity)
activity=activity[activity.activity_type!='last_closing_prob']
activity.head()
activity.info()

#creating the pivot table for the weekly view
activity['created_on']= pd.to_datetime(activity['created_on'])
grouped_df = activity.groupby(['activity_type','app', pd.Grouper(key='created_on', freq='W-MON')])['number'].count().reset_index().sort_values('created_on')
grouped_df_filtered=grouped_df[grouped_df['created_on'] >= datetime.datetime.now() - pd.to_timedelta("35day")]
grouped_df_filtered['created_on']=grouped_df_filtered['created_on'].dt.date
final_table=grouped_df_filtered.pivot(index=['app','activity_type'], columns='created_on', values='number')
final_table=final_table.reset_index()
final_table.columns = final_table.columns.astype(str)

############################### Here start the dashboard
import streamlit as st

st.set_page_config(layout="wide")
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
               .reportview-container .main .block-container{{
           padding-top: {padding_top}rem;
       }}
               .greeting h1 {
              font-family: 'Raleway', sans-serif;
              font-weight: lighter;
              font-size: 100px;
              text-align: center;
              margin: 0
            }
            .greeting h2 {
              font-family: 'Raleway', sans-serif;
              font-weight: lighter;
              font-size: 35px;
              text-align: center;
              margin: 0
            }
        </style>
        """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;margin: 0;'>Activities Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;margin: 0;'>Select a Podio App</h3>", unsafe_allow_html=True)
option = st.selectbox(
    #"<h3 style='text-align: center;'>Select a Podio App</h3>",
    #'Select a Podio App',
    '',
    activity['app'].unique(),)

#st.write('You selected:', option)

tab1, tab2 = st.tabs(["Main", "Correlation"])

with tab1:
   #st.header("A cat")

    col1, col2 = st.columns([3, 1])
    with col1:
        #creting the sum per row and per column
        #dt1=final_table
        dt1=final_table[final_table['app']==option]
        dt1.loc['Total',:]= dt1.sum(axis=0)
        dt1.loc[:,'Total'] =dt1.sum(axis=1)
        dt1.iat[len(dt1.index)-1,0]='Total'
        dt1.iat[len(dt1.index)-1,1]='Total'
        dt1 = dt1.reset_index(drop=True)
        #dt1.values=dt1.values.astype(int)
        dt1=dt1.fillna(0)
        for i in dt1.columns:
            try:
                dt1[[i]] = dt1[[i]].astype(float).astype(int)
            except:
                pass
#        dt1.info()
        hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        st.table(dt1.fillna(0))
        
    with col2:
        with st.container():
            df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [-33.86, 151.21],
            columns=['lat', 'lon'])
            st.map(df)
        
        #st.table(final_table)
    
    col3, col4 = st.columns([1, 3])
    with col3:
        df_syn = pd.DataFrame({'actvity_id' : ['contact_comment', 'create_contact', 'email_traceability', 'incoming_mail','outgoing_mail', 'deals_comment','deal_creation'],
                            'counter' : [10, 20, 30, 40,50,60,70],
                            'app' : ['Contacts','Contacts','Contacts','Contacts','Contacts','Deals','Deals']})
        st.table(df_syn[df_syn['app']==option])
    with col4:
        chart_data=activity.copy()
        chart_data=chart_data[chart_data['app']==option]
        pv = pd.pivot_table(chart_data, index=['created_on'], columns=["activity_type"], values=['number'], aggfunc=len, fill_value=0)
        pv.columns=pv.columns.droplevel()
        #chart_data.index=chart_data['created_on']
        #chart_data=chart_data.drop(['created_on','created_by.name','link','message'], axis=1)
        st.bar_chart(pv)

with tab2:
    t2col1, t2col2, t2col3 = st.columns(3)
    with t2col2:
        #corr_table=final_table
        corr_table=final_table[final_table['app']==option]
        corr_table=corr_table.drop('app', axis=1)
        corr_table=corr_table.fillna(0)
        corr_table=corr_table.T
        #corr_table=corr_table.astype(int)
        new_header = corr_table.iloc[0]
        corr_table = corr_table[1:] #take the data less the header row
        corr_table.columns = new_header
        corr_table=corr_table.astype(int)
        corr_table_res=corr_table.corr()
        import seaborn as sns
        import matplotlib.pyplot as plt
    #    fig, ax = plt.subplots(figsize=(2, 1))
        fig, ax = plt.subplots()
        sns.heatmap(corr_table_res, ax=ax)
        st.write(fig) 
    
   # st.table(corr_table_res)
    #st.table(final_table[final_table['app']==option].corr())

            
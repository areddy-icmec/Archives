import pandas as pd
import datetime
import numpy as np
from helpers import *
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

import streamlit as st
st.set_page_config( page_title = 'icmec weekly' ,  
                    page_icon="🧊",
                    layout="wide")



PodioData = GetData('''SELECT * FROM dev."podio_data";''') #this can be moded to get data only for 35 days 
#PodioData.loc[:,'created_on'] =   pd.to_datetime( PodioData.loc[:,'created_on']);
PodioData['activityType'] = PodioData['activityType'].replace({'item':'app entries','item_revision':'updates'})
PodioData['created_on'] =   pd.to_datetime( PodioData['created_on']);


def getUniqueAppName(df):
    return df['appName'].unique()

def getDataBasedOnOption(opt,df):
    filtered = df[df.appName == opt ]
    recentItems  = filtered[filtered['created_on'] >= datetime.datetime.now() - pd.to_timedelta("35day")]
    recentItemsGroupd = recentItems.groupby(['activityType',pd.Grouper(key='created_on', freq='W-MON')]).size()
    recentItemsGroupd = recentItemsGroupd.reset_index().pivot(index=['activityType'], columns='created_on', values=0)
    recentItemsGroupd =   recentItemsGroupd.fillna(0)
    recentItemsGroupd =  recentItemsGroupd[recentItemsGroupd.columns].astype(int)
    return recentItemsGroupd

def renameCols( groupedDf ):
    start = datetime.datetime.now() - pd.to_timedelta("35day")
    new_list  = [ start ]
    new_list.extend( groupedDf.columns[:-1] )
    new_col_list = []
    for e1,e2 in zip( new_list , groupedDf.columns ) :
        new_col_list.append(f"{e1.day}/{e1.month} - {e2.day}/{e2.month}") 
    return new_col_list

def getAllByOption(opt,df):
    filtered = df[df.appName == opt ] 
    groupedByActivityType =  filtered.groupby('activityType')[['activityType']].size() #we require this to put it in a table.  
    groupedByActivityType = groupedByActivityType.reset_index()
    groupedByActivityType.columns = ['Activity Type','Total']
    return groupedByActivityType

def makeBarPlot( opt , df ):
    filtered = df[df.appName == opt ]
    pTable = pd.pivot_table(filtered, index=['created_on'], columns=["activityType"], aggfunc=len, fill_value=0)
    return pTable['Name']

def getCorrelationMatrix( opt , df):
    recentItemsGroupd = getDataBasedOnOption(opt , df)
    corrT = recentItemsGroupd.T
    print('==='*30)
    if(corrT.shape[0] < 2 ):
        return 0
    print('==='*30)
    corrResults = corrT.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corrResults, ax=ax)
    return fig 


UniqueAppName = getUniqueAppName(PodioData)
random_data_for_map = pd.DataFrame(
                np.random.randn(1000, 2) / [50, 50] + [-33.86, 151.21],
                columns=['lat', 'lon'])

'''
LOGIN
'''

def dashcode():

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
        UniqueAppName,)

    tab1, tab2 = st.tabs(["Main", "Correlation"])

    with tab1:
    #st.header("A cat")

        col1, col2 = st.columns([3, 1])
        with col1:
            #creting the sum per row and per column
            #dt1=final_table

            dt1 = getDataBasedOnOption( opt = option , df= PodioData   )
            dt1.columns = renameCols(dt1)

            dt1.loc['Total',:]= dt1.sum(axis=0)
            dt1.loc[:,'Total'] =dt1.sum(axis=1)
            dt1 =  dt1[dt1.columns].astype(int)
            
            hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

            # Inject CSS with Markdown
            #st.markdown(unsafe_allow_html=True)
            
            st.table(dt1.replace(0,'-'))
            
        with col2:
            with st.container():
                st.map(random_data_for_map)
            
            #st.table(final_table)
        
        col3, col4 = st.columns([1, 3])
        with col3:
            df_syn = getAllByOption( opt= option , df=PodioData)
            st.table(df_syn)
        with col4:
            pv = makeBarPlot( opt=option , df=PodioData )
            st.bar_chart(pv)

    with tab2:
        t2col1, t2col2, t2col3 = st.columns(3)
        with t2col2:   
            fig =  getCorrelationMatrix(opt=option,df=PodioData)
            if(fig):
                st.write(fig)
            else:
                st.info("Not enough data to build Correlation matrix") 
        
    # st.table(corr_table_res)
        #st.table(final_table[final_table['app']==option].corr())

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username",  key="username")
        st.text_input(
            "Password", type="password",  key="password"
        )
        st.button("Login", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", key="username")
        st.text_input(
            "Password", type="password", key="password"
        )
        st.error("😕 User not known or password incorrect")
        st.button("Login", on_click=password_entered)
        return False
    else:
        # Password correct.
        return True

if check_password():    
    dashcode()
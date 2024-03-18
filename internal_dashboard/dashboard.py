#load libraries
import pandas as pd
import plotly.express as px

#read the pickle file

#filePath = 'G:/My Drive/Internal Dashboard/data/portal_data.pickle'
filePath  = '/Users/icmec/Documents/internal_dashboard/MemberPortalConnection/data/portalData.pickle'

obj = pd.read_pickle(filePath)

#create a series of all dates
all_dates = pd.date_range('14-07-2022', pd.to_datetime('today').normalize())
all_dates = pd.DataFrame(all_dates, columns=["date"])

#separate the data for each graph
numMembers = pd.DataFrame.from_dict(obj["numMembers"]) 
numMembers = numMembers.rename_axis('date').reset_index()
numMembers["date"] = pd.to_datetime(numMembers["date"])
numMembers = all_dates.merge(right=numMembers, how='left', on='date')
numMembers = numMembers.fillna(0)
numMembers["cumulative"]=numMembers["cnt"].cumsum().astype(int)

numInvitations = pd.DataFrame.from_dict(obj["numInvitations"]) 
numInvitations = numInvitations.rename_axis('date').reset_index()
numInvitations["date"] = pd.to_datetime(numInvitations["date"])
numInvitations = all_dates.merge(right=numInvitations, how='left', on='date')
numInvitations = numInvitations.fillna(0)
numInvitations["cumulative"]=numInvitations["cnt"].cumsum().astype(int)

numConnections = pd.DataFrame.from_dict(obj["numConnections"]) 
numConnections = numConnections.rename_axis('date').reset_index()
numConnections["date"] = pd.to_datetime(numConnections["date"])
numConnections = all_dates.merge(right=numConnections, how='left', on='date')
numConnections = numConnections.fillna(0)
numConnections["cumulative"]=numConnections["cnt"].cumsum().astype(int)

numMessages = pd.DataFrame.from_dict(obj["numMessages"]) 
numMessages = numMessages.rename_axis('date').reset_index()
numMessages["date"] = pd.to_datetime(numMessages["date"])
numMessages = all_dates.merge(right=numMessages, how='left', on='date')
numMessages = numMessages.fillna(0)
numMessages["cumulative"]=numMessages["cnt"].cumsum().astype(int)
numMessages.info()

############################### Here start the dashboard
import streamlit as st

#page conf and reduce blank space
st.set_page_config(page_title='Internal Dashboard',
                   page_icon='https://miro.medium.com/max/2400/1*AT3QhJbUnYbA3eMWVE7cLA.png',
                   layout="wide")

padding_top = 0

st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

#title
st.title('Internal Dashboard')

tab1, tab2, tab3 = st.tabs(["Members", "Portal Traffic Behaviour", "LinkedIn"])

#tab1
with tab1:
    import streamlit as st
    
    d = st.date_input(
        "Select a date to analise",
        pd.to_datetime('today').normalize())
        
    column1, column2, column3, column4  = st.columns(4)
    with column1:
        st.metric(label="Members", value=numMembers.loc[numMembers['date']== d.isoformat()].cumulative, 
                  help="Number of members in the member portal on "+d.isoformat()) # , delta="1.2 °F")
    with column2:
        # st.metric(label="Connections", value=numConnections.loc[numConnections['date']== pd.to_datetime('today').normalize()].cumulative,
        #           help="Total number of user connections in the member portal") # , delta="1.2 °F")

        st.metric(label="Connections", value=numConnections.loc[numConnections['date']== d.isoformat()].cumulative,
                  help="Total number of user connections in the member portal on "+d.isoformat()) # , delta="1.2 °F")
    with column3:
        st.metric(label="Invitations", value=numInvitations.loc[numInvitations['date']== d.isoformat()].cumulative,
                  help="Total number of user invitations in the member portal on "+d.isoformat()) # , delta="1.2 °F")
    with column4:
        st.metric(label="Messages", value=numMessages.loc[numMessages['date']== d.isoformat()].cumulative,
                  help="Total number of user accounts in the member portal on "+d.isoformat()) # , delta="1.2 °F")


    #Graphs in new 2 rows 2 col
    col1, col2 = st.columns(2)
    
    with col1:
        #graph1
                
        fig = px.line(numMembers, x='date', y="cumulative", title="ID2 - What is the total number of members?", markers=False).update_layout(
        yaxis_title="Total")#, yaxis_title="7 day avg")
                   #labels=dict(x="aaaaaaaaaaaaa", y="Amount", color="Place"))
        
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        #graph2
        import plotly.express as px
        
        fig = px.line(numInvitations, x='date', y="cnt", title="ID24 - What is the average number of invitations per member? (for now is the count per day)", markers=False).update_layout(
        yaxis_title="Count")#, yaxis_title="7 day avg")
                   #labels=dict(x="aaaaaaaaaaaaa", y="Amount", color="Place"))
        
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    with col2:
        #graph3
      import plotly.express as px
       
      fig = px.line(numConnections, x='date', y="cnt", title="ID25 - What is the average number of connections per member? (for now is the count per day)", markers=False).update_layout(
      yaxis_title="Count")#, yaxis_title="7 day avg")
                 #labels=dict(x="aaaaaaaaaaaaa", y="Amount", color="Place"))
      
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)

      #graph4
      
      import plotly.express as px
       
      fig = px.line(numMessages, x='date', y="cnt", title="ID23 - What is the average number of messages per member? (for now is the count per day)",markers=False).update_layout(
      yaxis_title="Count")#, yaxis_title="7 day avg")
                 #labels=dict(x="aaaaaaaaaaaaa", y="Amount", color="Place"))
      
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)


with tab2:
    st.subheader("Google Analytics related metrics")
    #st.markdown('<b>Must Have metrics</b>', unsafe_allow_html=True)
    st.markdown('<iframe width="1100" height="1100" src="https://lookerstudio.google.com/embed/reporting/cf663925-d125-496d-9404-c1463009408e/page/CwMED" frameborder="0" style="border:0" allowfullscreen></iframe>', unsafe_allow_html=True)

with tab3:
    
    st.subheader("Linkedin related metrics")
    
    st.markdown('<a href="https://www.linkedin.com/company/81773610/admin/analytics/visitors/">Visitor highlights - How many LinkedIn page views do we have?</a>', unsafe_allow_html=True)
    
    st.markdown('<a href="https://www.linkedin.com/company/81773610/admin/analytics/followers/">Followers highlights - How many LinkedIn followers do we have?</a>', unsafe_allow_html=True)

    st.markdown('<a href="https://www.linkedin.com/company/81773610/admin/analytics/updates/">Content Analytics - How many LinkedIn content impressions (visits) do we have?</a>', unsafe_allow_html=True)


import pandas as pd

df=pd.read_csv(r'G:\My Drive\Project Castle\data\filtered.csv')
print(df)
df.info()
df['user_email'].head()
df['username'].head()
df=df.filter(items=['username', 'user_email', 'user_timezone','user_rank'])
#converting time stamps
#pd.to_datetime(df.user_regdate.head()   , unit= 's' )

import streamlit as st

#st.set_page_config(page_title='Project Castle', layout = 'wide', page_icon = 'https://www.freepnglogos.com/uploads/castle-png/haunted-castle-transparent-picture-19.png', initial_sidebar_state = 'auto')
st.set_page_config(page_title='Project Castle', page_icon = 'https://www.freepnglogos.com/uploads/castle-png/haunted-castle-transparent-picture-19.png', initial_sidebar_state = 'auto')


col1, col2 = st.columns([1,2])
with col1:
    st.header('Project Castle')
with col2:
    st.image('https://www.freepnglogos.com/uploads/castle-png/haunted-castle-transparent-picture-19.png', width=70)

####Data Products
tab1, tab2, tab3 = st.tabs(["Username", "pCard", "Analytics"])

with tab1:
   
    ######username match
    #st.subheader("Search a username")
    # st.write("Enter a username to find out if it is in the database")
     
    username_input = st.text_input('Enter a username to find out if it is in the database', 'e.g. NewBee')
    
    if username_input != "e.g. NewBee":
            
        #exact match
        st.subheader('Exact match')
         
        data_table_exact=df[df['username']==username_input].filter(items=['username', 'user_email', 'user_timezone'])
        
        # CSS to inject contained in a string (remove ids from table)
        hide_table_row_index = """
                     <style>
                     thead tr th:first-child {display:none}
                     tbody th {display:none}
                     </style>
                     """
        
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        # Display a static table
        st.table(data_table_exact)
       
       
    
        #####case insensitive
        st.subheader('Case insensitive')
        username_input=str(username_input)
        
        data_table_case=df[df['username'].str.casefold()==username_input.casefold()].filter(items=['username', 'user_email', 'user_timezone'])
        
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
        
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        # Display a static table
        st.table(data_table_case)
        
        #####similar distance Levenshtein_Distance
        st.subheader('Similarity: Levenshtein Distance')
        username_input=str(username_input)
        
        #calculate the distance with all the usernames in the db
        import jellyfish
        #jellyfish.levenshtein_distance(u'NewBee', df['username'].iloc[0])
        
        df['L_distance']=df.apply(lambda x: jellyfish.levenshtein_distance(username_input,  x['username']), axis=1)
        
        #only show the closest ones (d<=2)
        data_table_case=df[df['L_distance']<=2].filter(items=['username', 'user_email', 'user_timezone','L_distance'])
        
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
        
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        # Display a static table
        st.table(data_table_case)
        #Damerau–Levenshtein distance
        
        #####similar distance jaro_winkler
        st.subheader('Similarity: Jaro Winkler Similarity')
        username_input=str(username_input)
        
        ####calculate the distance 
        df['JW_distance']=df.apply(lambda x: jellyfish.jaro_winkler_similarity(username_input,  x['username']), axis=1)
        
        #select the closer ones
        data_table_case=df[df['JW_distance']>=0.85].filter(items=['username', 'user_email', 'user_timezone','JW_distance']).sort_values(by='JW_distance',ascending=False)
        
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
        
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        # Display a static table
        st.table(data_table_case)

with tab2:
   #st.header("An owl")
   #st.write("Enter a username to find out if it is in the database")
   
   df=pd.read_csv(r'G:\My Drive\Project Castle\data\filtered.csv')
   
   username_input2 = st.text_input('Enter a username to find out related information from our databases', 'e.g. NewBee')
   
   if username_input2 != "e.g. NewBee":

       selected_data=df[df['username']==username_input2]
    
       ##add map data
       cities_data=pd.read_csv('G:\My Drive\Project Castle\data\cities_lat_lon_quantity.csv')
       joined=selected_data.merge(cities_data, on='user_timezone', how='left')
    
       st.markdown(f"username: {str(selected_data.username.values).strip('[').strip(']')}", unsafe_allow_html=False)
       st.markdown(f"email: {str(selected_data.user_email.values).strip('[').strip(']')}", unsafe_allow_html=False)
       st.markdown(f"timezone: {str(selected_data.user_timezone.values).strip('[').strip(']')}", unsafe_allow_html=False)
       st.markdown(f"latitude: {str(joined.lat.values).strip('[').strip(']')}", unsafe_allow_html=False)
       st.markdown(f"longitude: {str(joined.lon.values).strip('[').strip(']')}", unsafe_allow_html=False)
       st.markdown(f"rank number: {str(selected_data.user_rank.values).strip('[').strip(']')}", unsafe_allow_html=False)
       st.markdown(f"rank title: {str(selected_data.rank_title.values).strip('[').strip(']')}", unsafe_allow_html=False)
    
       st.map(joined[["lon","lat"]])
       
       ##flairs
       st.write("Username Flairs:")
       path=r'G:\Shared drives\ICMEC Australia\Stream 2 - Data Product\Project CASTLE\phpbb_flair_users.json'
       # read the json file
       import pandas as pd
       import orjson
       data = [orjson.loads(line) for line in open(path, 'r', encoding="utf8")]
       flairs_users=pd.DataFrame(data)
       print(flairs_users)
       flairs_users.info()

       df2=pd.read_csv(r'G:\My Drive\Project Castle\data\filtered.csv')

       # joined_rank=data_extract.merge(ranks, on='user_rank', how='left')
       users_flair=df2.merge(flairs_users, on='user_id', how='left')

       path=r'G:\Shared drives\ICMEC Australia\Stream 2 - Data Product\Project CASTLE\phpbb_flair.json'
       # read the json file
       import pandas as pd
       import orjson
       data = [orjson.loads(line) for line in open(path, 'r', encoding="utf8")]
       flairs=pd.DataFrame(data)
       print(flairs)
       flairs.info()

       # joined_rank=data_extract.merge(ranks, on='user_rank', how='left')
       users_flair_flair=users_flair.merge(flairs, on='flair_id', how='left')
       
       # CSS to inject contained in a string
       hide_table_row_index = """
                   <style>
                   thead tr th:first-child {display:none}
                   tbody th {display:none}
                   </style>
                   """
       
       # Inject CSS with Markdown
       st.markdown(hide_table_row_index, unsafe_allow_html=True)
       
       #show the table
       st.table(users_flair_flair[users_flair_flair['username']==username_input2].filter(items=['username', 'flair_name', 'flair_desc']))
       #df[df['username']==username_input2]
   
with tab3:
   #st.write("Enter a username to find out if it is in the database")

   ## MAP
   import streamlit as st
   import pandas as pd
   #import numpy as np
   import pydeck as pdk
   
   # Set viewport for the deckgl map
   view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

   mydata=pd.read_csv('G:\My Drive\Project Castle\data\cities_lat_lon_quantity.csv')
   #drop.NA
   mydata = mydata.dropna()

   mydata=mydata[["city","lon","lat","size"]]

   mydata["size2"]=mydata["size"]*500

   #st.subheader("Map")
   st.write("The following map display the location of ", mydata["size"].sum(),
            " user accounts, which represent ", round((mydata["size"].sum()/len(df.index))*100,1),
            "% of the total user account in our databases.",
            "Is important to highlight a person can have more than one user account and the locations (cities) where determined using the users accounts' UTC")
   # Create the scatter plot layer
   covidLayer = pdk.Layer(
           "ScatterplotLayer",
           data=mydata,
           pickable=True,
           opacity=0.5,
           stroked=True,
           filled=True,
           radius_scale=6,
           radius_min_pixels=1,
           radius_max_pixels=100,
           line_width_min_pixels=1,
           get_position=["lon", "lat"],
           get_radius=["size2"],
           get_fill_color=[252, 136, 3],
           get_line_color=[0,0,0],
           tooltip="test test",
       )

   # Create the deck.gl map
   r = pdk.Deck(
       layers=[covidLayer],
       initial_view_state=view,
       map_style="mapbox://styles/mapbox/light-v10",
       tooltip={"text": "{city}:{size}"},
   )

   # Render the deck.gl map in the Streamlit app as a Pydeck chart 
   # def filter_by_viewport(widget_instance, payload):
   #     try:
   #         west_lng, north_lat = payload['data']['nw']
   #         east_lng, south_lat = payload['data']['se']
   #         filtered_df = df[df.apply(lambda row: filter_by_bbox(row, west_lng, east_lng, north_lat, south_lat), axis=1)]
   #         text.value = 'Points in viewport: %s' % int(filtered_df.count()['lng'])
   #     except Exception as e:
   #         text.value = 'Error: %s' % e

   # from ipywidgets import HTML
   # def one_f(widget_instance, payload):
   #     text=payload

   # r.deck_widget.on_click(one_f)
   # display(text)


   map = st.pydeck_chart(r)

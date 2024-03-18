# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 14:54:43 2022

@author: cladi
"""

import streamlit as st
import pandas as pd

#set the page config in streamlit
st.set_page_config(
    page_title="Utility Tools Catalogue",
    page_icon="https://miro.medium.com/max/2400/1*AT3QhJbUnYbA3eMWVE7cLA.png",
    layout="wide",
)

st.title('Utility Tools Catalogue')

#Read the data from the excel, eventually this should be replaced to a DB connection
data=pd.read_excel("data.xlsx", "Sheet1", index_col=False)

data=data.reset_index(drop=True)

#create the dropdown
type_of_data = data['Type of Data'].unique().tolist()
container = st.container()
sel_all = st.checkbox("Select all")

if sel_all:
    type_of_data_selected = container.multiselect("Select the type of data you're looking for", type_of_data,type_of_data)
else:
    type_of_data_selected = container.multiselect("Select the type of data you're looking for", type_of_data)


selected_data = data['Type of Data'].isin(type_of_data_selected)

#print the table
st.markdown(
    data[selected_data].to_html(escape=False, index=False).replace('<th>', '<th align="left">'),
    unsafe_allow_html=True
)

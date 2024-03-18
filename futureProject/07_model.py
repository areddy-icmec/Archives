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

# local
directory="G:\My Drive\Project Lighthouse\project_lighthouse\webApp\helpers\queries.py"

# #ec2
# directory="/home/ubuntu/project_crc/webApp/queries.py"

with open(directory) as infile:
    exec(infile.read())
    
def code():
    st.set_page_config(
        page_title='Project Lighthouse', 
        page_icon = 'https://miro.medium.com/max/2400/1*AT3QhJbUnYbA3eMWVE7cLA.png'
        )

    col1, col2 = st.columns([6,8])
    # col1, col2 = st.columns(2, gap = "small")
    with col1:
        st.header('Project Lighthouse')
    with col2:
        st.image('https://upload.wikimedia.org/wikipedia/commons/9/9b/Lighthouse_icon.svg', width=50)

    import pandas as pd
    # date_initial = pd.to_datetime('01-01-2023').normalize()
    # # time_initial = datetime.time(00, 00)
    # date_end = pd.to_datetime('21-06-2023').normalize()
    # # time_end = datetime.time(23, 45)

    # # selected_time_range_ini="{} {}".format(date_initial,time_initial)
    # # selected_time_range_end="{} {}".format(date_end,time_end)
    # selected_time_range_ini=date_initial
    # selected_time_range_end=date_end
    
    #input for the search option
    specific_guid = st.text_input('Enter a guid to find out if it is in the database', 'e.g. 00037CA9885DEE48A6BFB3703562AAA1')

    # specific_guid='26FAE195D7C05841875AAD1765D9744E'
    # specific_guid='00037CA9885DEE48A6BFB3703562AAA1'
    # especific_guid='000AC4B65C83CC4A801D4D726DDE9E06'
    # especific_guid='000DDEA0720EAD9A695DFBCB12E46FF5'
    ####################################################################Datasets
    # %%
    
    if specific_guid != 'e.g. 00037CA9885DEE48A6BFB3703562AAA1':
        ####Query for the data
        prediction_data_res=crc_guid_exact_match(specific_guid)
        #select only timestamp
        selected_features=pd.to_datetime(prediction_data_res['timestamp_utc'])
        selected_features=pd.DataFrame(selected_features)
        # selected_features

        ###Modelling to transform minute detections to daily
        #create date from timestamp
        selected_features['date']=selected_features['timestamp_utc'].dt.date
        #sort by date desc
        selected_features=selected_features.sort_values(by=['date'], ascending=False)
        #group by date and count
        selected_features=selected_features.groupby(['date']).count().reset_index()
        #rename colum name to count
        selected_features.columns=['date','count']

        ###generate the time series for days without detections
        #min max dates
        min_date=selected_features['date'].min()
        max_date=selected_features['date'].max()

        #create a list of dates between min and max date
        date_list = pd.date_range(min_date, max_date).tolist()

        #create a dataframe with all the dates
        date_df = pd.DataFrame(date_list, columns=['date'])

        #transform date to date
        date_df['date']=date_df['date'].dt.date
        # selected_features['date']=selected_features['date'].dt.date

        #merge the date_df with the selected_features
        selected_features=pd.merge(date_df, selected_features, on='date', how='left')

        #fill the nan values with 0
        selected_features=selected_features.fillna(0)
        # selected_features

        # %%
        ### create the target feature
        #if selected_features['count']>0 then 1, else 0
        selected_features['target'] = selected_features['count'].apply(lambda count: 1 if count > 0 else 0)
        #drop the count column
        selected_features=selected_features.drop(['count'], axis=1)

        #create time features
        #transform date to datetime
        def create_features(df):
            df['date']=pd.to_datetime(df['date'])
            #year
            df['year']=df['date'].dt.year
            #month
            df['month']=df['date'].dt.month
            #day
            df['day']=df['date'].dt.day
            #week of year
            df['week']=df['date'].dt.weekofyear
            #day of the week
            df['day_of_week']=df['date'].dt.dayofweek
            #is weekend
            df['is_weekend']=df['day_of_week'].apply(lambda x: 1 if x>4 else 0)
            #week of the month
            df['week_of_month']=df['date'].dt.week
            
            ####lag features
            # number of values in date_list
            # lags = range(1, len(date_list)+1)
            # for lag in lags:
            #     df[f'lag{lag}'] = df['target'].shift(lag)

            return df

        #drop date
        selected_features_all = create_features(selected_features)
        # selected_features_all
        selected_features=selected_features_all.drop(['date'], axis=1)
        # selected_features

        # Create a XGBoost model to predict the next detection
        # %%
        #import xgboost
        from sklearn.model_selection import train_test_split

        # Extract feature and target arrays
        X, y = selected_features.drop('target', axis=1), selected_features[['target']]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, train_size=.25, shuffle=True) #25% for testing

        # %%
        #model
        import xgboost as xgb

        # Train a model using the scikit-learn API
        xgb_model = xgb.XGBClassifier(n_estimators=100,random_state=123)
        # xgb_model = xgb.XGBClassifier(n_estimators=100, objective='binary:logistic', random_state=123)

        xgb_model.fit(X_train, y_train)

        # xgb_model.fit(X, y)

        y_pred = xgb_model.predict(X_test)

        from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
        # st.write(confusion_matrix(y_test, y_pred))

        # %%
        #validation
        from sklearn.model_selection import cross_val_score, KFold
        import numpy as np

        scores = cross_val_score(xgb_model, X, y, scoring="accuracy", cv=5)
        # st.write(scores)
        st.write("Model cross-validation mean accurracy: ", scores.mean().round(3)*100,"%")
        st.write("Model accuracy: ",accuracy_score(y_test,y_pred))

        # %%
        import matplotlib.pylab as plt
        from xgboost import plot_importance
        importance=plot_importance(xgb_model, max_num_features=10) # top 10 most important features
        # st.pyplot(plt.gcf())

        # %%
        #plot real vs prediction
        y_pred = xgb_model.predict(X)

        # selected_features_all = pd.DataFrame(columns=['date', 'count'])
        selected_features_all['pred'] = y_pred
        # st.write(selected_features_all)

        #if count and pred are the same then 1
        selected_features_all['same']='0'
        selected_features_all.loc[selected_features_all['target'] == selected_features_all['pred'], 'same'] = 'yes'
        #if selected_features_all['same']=='0' then 'no'
        selected_features_all.loc[selected_features_all['same']=='0', 'same'] = 'no'
        # st.write(selected_features_all)

        import plotly.express as px
        fig = px.scatter(selected_features_all, x='date', y='target', color='same', color_discrete_sequence=["red", "green"],
             category_orders={"same": ["no", "yes"]},)
        st.plotly_chart(fig)

        # %%
        #Predict the following 14 days
        #pick the max date
        import pandas as pd
        last_date=selected_features_all.date.max()
        # st.write(last_date)

        #add 14 days from max_date as series
        next_two_weeks=last_date+pd.DateOffset(days=14)
        # st.write(next_two_weeks)

        #create a list of dates between min and max date
        date_list = pd.date_range(last_date+pd.DateOffset(days=1), next_two_weeks).tolist()

        #create a dataframe with all the dates
        dates_df = pd.DataFrame(date_list, columns=['date'])
        #trassform date to date
        # dates_df['date']=date_df['date'].dt.date
        # st.dataframe(dates_df)



        # %%
        #create the features using the next two weeks

        next_two_weeks_features=create_features(dates_df)
        # st.dataframe(next_two_weeks_features)
        
        #delete colum date
        next_two_weeks_features=next_two_weeks_features.drop(['date'], axis=1)
        #plot real vs prediction
        y_pred_next_two_weeks = xgb_model.predict(next_two_weeks_features)

        next_two_weeks_features['pred'] = y_pred_next_two_weeks
        # st.write("Next days predictions")
        next_two_weeks_features['date']=dates_df['date']
        # st.dataframe(next_two_weeks_features)        
        import plotly.express as px
        fig = px.scatter(next_two_weeks_features, x='date', y='pred')
        st.write("Plot of the forecast of the new connections")
        st.plotly_chart(fig)
        
        # aer2=pd.concat([selected_features_all, next_two_weeks_features])
        # #replace null with "prediction"
        # aer2['same'] = aer2['same'].fillna('prediction')
        # # aer2['target'] = aer2['target'].fillna(3)
        # st.write("*********")
        # st.dataframe(aer2)
        
        # import plotly.express as px
        # fig = px.scatter(aer2, x='date', y='target', color='same', color_discrete_sequence=["red", "green",'blue'],
        #      category_orders={"same": ["no", "yes","prediction"]},)
        # st.plotly_chart(fig)


        # ###########is gicing all 0, which can be the case
        # #######test with other guids

        # ####test adding the lags as features
        # ####for that we need to add the lag features in the function, and add the original dataframe to dates_df (append? left join?)

        # # aer=selected_features.merge(dates_df, how='left', on='date')
        # aer=selected_features_all.copy()
        # # dates_df['target']=0
        # aer=aer.append(dates_df)
        # aer=create_features(aer)
        # # st.dataframe(aer)
        # #drop pred and same
        # aer2=aer.drop(['target','pred','same'], axis=1)
        # aer=aer.drop(['target','pred','same', 'date'], axis=1)
        # st.write("Next days with features:")
        # st.dataframe(aer)
        
        # aer['pred'] = xgb_model.predict(aer)
        # st.write("Next days predictions")
        # st.dataframe(aer)
        # # aer['original_target']=selected_features_all['target']
        # # aer['original_pred']=selected_features_all['pred']
        # # st.dataframe(aer)
        
        # import plotly.express as px
        # fig = px.scatter(aer, x='date', y='target', color='same', color_discrete_sequence=["red", "green"],
        #      category_orders={"same": ["no", "yes"]},)
        # st.plotly_chart(fig)
        
        # # #add col same ('yes' or 'no'), and for the 2 weeks add 'forecasted'
        # # #left join select all
        # # aer=aer.merge(selected_features_all[['date','target','pred','same']], how='left', on='date')
        # # import plotly.express as px
        # # fig = px.scatter(aer, x='date', y='target', color='same', color_discrete_sequence=["red", "green"],
        # #      category_orders={"same": ["no", "yes"]},)
        # # st.plotly_chart(fig)


if check_password():    
    code()
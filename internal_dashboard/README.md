# Internal Dashboard

The internal dashboard objective is to deliver insights to enable the ICMEC Australia team to make informed decisions. It display metrics relevant for the different streams.

# Framework
The ETL is written in Python, as well as the dashboard. The framework used for the dashboard is streamlit.

# ETL process
We are connecting directly to the production database in a daily basis. We created SQL queries to extract the data. The data is stored momentarily in json files in the VM. The dashboard read the files and make the graphs.  

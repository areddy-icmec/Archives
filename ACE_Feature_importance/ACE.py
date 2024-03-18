import pandas as pd
import numpy as np
#ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Import the os module
import os

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# Change the current working directory
os.chdir('G:/My drive/NSW Offences/Scripts/')

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

import pipeline

#read connection credentials
credentials=pd.read_excel("G:/My drive/NSW Offences/Scripts/connection.xlsx")

query_string=""" SELECT * FROM prod."2021_census.gcp_all_juvenile_victims.lga"  """
print(query_string)
original_data = pipeline.do_query(query_string, credentials.user.iloc[0],credentials.password.iloc[0], credentials.host.iloc[0],credentials.port.iloc[0], credentials.database.iloc[0])
#original_data=pd.read_csv('https://data-lake-icmec-au.s3.ap-southeast-2.amazonaws.com/projectCrimeCensus/2021_census.gcp_all_juvenile_victims.lga.csv')
original_data=original_data.set_index('index')
original_data.columns
original_data=original_data.T
#original_data.columns = original_data.iloc[0] 
#original_data=original_data[1:]
model_data=original_data.copy()
model_data
model_data=model_data.drop(['lga_code_2021'], axis=1)
model_data.head()
x=model_data.columns
x=pd.DataFrame(x)
x.to_csv('columns.csv')
model_data.columns

#divide the df into census and bocsar
len(model_data.columns)
bocsardata=model_data.iloc[:,-22:].copy()
censusdata=model_data.iloc[:,:len(model_data.columns)-22].copy()

#stats from data
# from pandas_profiling import ProfileReport
# profile = ProfileReport(bocsardata, title="Pandas Profiling Report")
# profile.to_file("data.html")

#censusdata.str.find('..')
#test = censusdata.select_dtypes([np.object]).apply(lambda x: x.str.contains('..').any())
#test
#select feature to be modelled
#target_feature='domestic_violence_related_assault.rate'
target_feature='domestic_violence_related_assault.count'
model_data=pd.concat([censusdata,bocsardata[[target_feature]]], axis=1)
model_data.columns
model_data.dtypes
censusdata.dtypes
censusdata.info()
#Do the correlation
corr_data=model_data.copy()
#corr_table=corr_data.corr()


#####################################Here is the ACE algo
#I dont know why is this not working, the data seems correct
x=censusdata.fillna(0)
x=x.astype(float)
x=x.astype(int)
x.dtypes.to_excel("test.xlsx")
#https://github.com/partofthething/ace
#https://partofthething.com/ace/#using-it
#https://partofthething.com/ace/apidoc/ace.samples.html#module-ace.samples.breiman85
from ace import ace
censusdata.isnull().sum().sum()
x=[*x.to_numpy()]#.fillna(0).values
y=bocsardata[[target_feature]]
ace_solver = ace.ACESolver()
ace_solver.specify_data_set(x, [y])
MAX_OUTERS = 200*1000
ace_solver.solve()

###################################Here are some examples of the algo working

from ace import model
myace = model.Model()
myace.build_model_from_xy([x], y)
myace.eval([0.1, 0.2, 0.5, 0.3, 0.5])

from ace.samples import wang04
x, y = wang04.build_sample_ace_problem_wang04(N=200)
from ace import model
myace = model.Model()
myace.build_model_from_xy(x, y)
myace.eval([0.1, 0.2, 0.5, 0.3, 0.5])
from ace import ace
ace.plot_transforms(myace.ace, fname = 'mytransforms.pdf')
myace.ace.write_transforms_to_file(fname = 'mytransforms.txt')

import numpy
import numpy.random
import scipy.special
from .. import ace
numpy.random.seed(9287349087)

[docs]def build_sample_ace_problem_breiman85(N=200):
    """
    Sample problem from Breiman 1985
    """
    x3 = numpy.random.standard_normal(N)
    x = scipy.special.cbrt(x3)
    noise = numpy.random.standard_normal(N)
    y = numpy.exp((x ** 3.0) + noise)
    return [x], y


[docs]def run_breiman85():
    x, y = build_sample_ace_problem_breiman85(200)
    ace_solver = ace.ACESolver()
    ace_solver.specify_data_set(x, y)
    ace_solver.solve()
    try:
        ace.plot_transforms(ace_solver, 'sample_ace_breiman85.png')
    except ImportError:
        pass

    return ace_solver

if __name__ == '__main__':
    run_breiman85()


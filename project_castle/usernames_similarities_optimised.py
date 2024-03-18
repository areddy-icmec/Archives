#!/usr/bin/env python
# coding: utf-8

# ### The objective is to determine whether the offenders have related usernames, for instance if they contain specific keywords.

# ### Read usernames

# In[1]:



# ### Select n=8k usernames

# In[2]:
    
import pandas as pd

n_data = 1000
    
df = pd.read_csv(r'G:\My Drive\Project Castle\data\filtered.csv')
#df=df.sample(n_data)
df=df.head(n_data)
df=df.filter(items=['username'])
df.head(3)

# ### Calculate Jaro-Winkler similarity

# <a href="https://srinivas-kulkarni.medium.com/jaro-winkler-vs-levenshtein-distance-2eab21832fd6">Here is a detailed explanation of the calculation</a>

# In[3]:
# get the start time

import time
from jarowinkler import *
from rapidfuzz import process

# get the start time
st = time.time()

#calculate the distance
sim_mat=process.cdist(df['username'], df['username'], scorer=jarowinkler_similarity)

# get the end time
et = time.time()

# get the execution time
elapsed_time_d = et - st
print('Distance execution time:', elapsed_time_d, 'seconds')


# visualise

# In[4]:

from sklearn.cluster import AffinityPropagation

# get the start time
st = time.time()

affprop = AffinityPropagation(affinity="precomputed", damping=0.9)
affprop.fit(sim_mat)

# get the end time
et = time.time()

# get the execution time
elapsed_time_a = et - st
print('Affinity execution time:', elapsed_time_a, 'seconds')


results=pd.DataFrame(affprop.labels_, columns=['cluster'])
results['center']=affprop.cluster_centers_indices_[results['cluster']]
results['center_word']=df.username.to_numpy()[affprop.cluster_centers_indices_[results['cluster']]]
results['word']=df['username'].reset_index(drop=True)
results

# results.to_csv(r'G:\My Drive\Project Castle\data\result_cluster_usernames.csv', index=False)

# print('clusters saved')


# # results.groupby(['cluster'], ['center']).count()
# df_grouped=results.groupby(['cluster', 'centers','centers_words']).size().reset_index(name='counts')    
# #df_grouped
# df_grouped.sort_values(by=['counts'], inplace=True, ascending=False)
# df_grouped.head(10)


# for cluster_id in df_grouped.head(10).cluster:
#     printing=', '.join(results[results['cluster']==cluster_id].words) 
    
#     # # Adding all the values
#     # res = ', '.join(df['word'])
    
#     # Display result
#     print('Cluster ',df_grouped[df_grouped['cluster']==cluster_id].values,'(id:',cluster_id,'):\n',printing,'\n')


### Cluster using Kmeans

#<a href="https://www.geeksforgeeks.org/affinity-propagation-in-ml-to-find-the-number-of-clusters/">Here is a detailed explanation of the calculation</a>

#Test

from sklearn.manifold import TSNE
projection = TSNE().fit_transform(sim_mat)
# import matplotlib.pyplot as plt
# plot_kwds = {'alpha' : 0.25, 's' : 10, 'linewidths':0}
# plt.scatter(*projection.T, **plot_kwds)
proj_df=pd.DataFrame(projection)
# proj_df.to_csv(r'G:\My Drive\Project Castle\data\result_cluster_usernames_projected.csv', index=False)

all_df=pd.concat([results, proj_df], axis=1)
all_df.rename(columns={0: "dim_0", 1:"dim_1"}, inplace=True)
# all_df

pd.DataFrame(all_df).to_csv(r'G:\My Drive\Project Castle\data\result_cluster_usernames_projected.csv', index=False)

print('projection saved')

# #Getting unique labels
# u_labels = np.unique(affprop.labels_)

# asdf=projection
# asdf=pd.DataFrame(asdf)
# asdf['cluster']=results['cluster']
# #plotting the results:
# asdf[asdf['cluster']==0]
# asdf.loc[asdf['cluster']==0,0]
# for i in u_labels:
#     plt.scatter(asdf.loc[asdf['cluster']==i ,0] , asdf.loc[asdf['cluster']==i , 1] , label = i)
# plt.legend()
# plt.show()
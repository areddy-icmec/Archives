########################user usernames
#path for the local json file
path=r'C:\Users\cladi\OneDrive\Escritorio\Data Project\phpbb_users copy.json'

# read the json file
import pandas as pd
import orjson
data = [orjson.loads(line) for line in open(path, 'r', encoding="utf8")]
df=pd.DataFrame(data)
print(df)
df.info()
df['user_email'].head()
df['username'].head()

#filter only the columns needed (for speed purposes)
data_extract=df.filter(items=['user_id','username', 'user_email', 'user_timezone','user_rank'])

# #save for later analysis
# data_extract.to_csv(r'G:\My Drive\Project Castle\data\filtered.csv',index=False)

####add user_ranks
#read user-ranks
#path for the local json file
path=r'G:\Shared drives\ICMEC Australia\Stream 2 - Data Product\Project CASTLE\phpbb_ranks.json'
# read the json file
import pandas as pd
import orjson
data = [orjson.loads(line) for line in open(path, 'r', encoding="utf8")]
ranks=pd.DataFrame(data)
print(ranks)
ranks.info()

#filter only the columns needed (for speed purposes)
ranks=ranks.filter(items=['rank_id', 'rank_title'])
ranks.rename(columns = {'rank_id':'user_rank'}, inplace = True)

# rank=pd.read_csv(r'G:\My Drive\Project Castle\data\pcard_data.csv')
joined_rank=data_extract.merge(ranks, on='user_rank', how='left')

# #save for later analysis
joined_rank.to_csv(r'G:\My Drive\Project Castle\data\filtered.csv',index=False)

######################cities lat lon
#read the data
import pandas as pd
df=pd.read_csv(r'G:\My Drive\Project Castle\data\filtered.csv')
print(df)
df.info()
#df['username']=df['username'].astype(str)
# df['user_email'].head()
# df['username'].head()
# print(df)
# df.info()
# df['user_timezone']
# df['user_timezone'].unique()

#grouped_data=df.groupby(['user_timezone']).count()
grouped_data=df.groupby(['user_timezone'], as_index=False).size()

new = grouped_data['user_timezone'].str.split("/", n = 1, expand = True)

grouped_data['continent']=new[0]
grouped_data['city']=new[1]

grouped_data.head()

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_user_agent")
city ="London"
country ="Uk"
loc = geolocator.geocode(city+','+ country)
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)


city ="antartica"
loc = geolocator.geocode(city)
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)

# grouped_data['lat']=geolocator.geocode(grouped_data['city'].loc[1]).latitude
# grouped_data['lon']=geolocator.geocode(grouped_data['city'].head()).longitude

grouped_data['continent'].unique()
unique_cities=grouped_data['city'].unique()
unique_cities=pd.DataFrame(unique_cities, columns=['city'])
list_lat = []   # create empty lists
list_long = []

#replace DumontDUrville with antartica
#unique_cities[unique_cities['city']=='DumontDUrville']
unique_cities[unique_cities['city']=='DumontDUrville']='antartica'


for index, row in unique_cities.iterrows():
    print(row.city)
    list_lat.append(geolocator.geocode(row.city).latitude)
    list_long.append(geolocator.geocode(row.city).longitude)

# unique_cities['lat'] = [geolocator.geocode(x).latitude for x in unique_cities[1]]
# unique_cities['lon'] = [geolocator.geocode(x).longitude for x in unique_cities]

unique_cities['lat'] = list_lat   
unique_cities['lon'] = list_long

unique_cities.to_csv(r'G:\My Drive\Project Castle\data\cities_lat_lon.csv',index=False)

final=grouped_data.merge(unique_cities, on='city', how='left')
final.to_csv(r'G:\My Drive\Project Castle\data\cities_lat_lon_quantity.csv',index=False)

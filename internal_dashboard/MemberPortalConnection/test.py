# LOAD
import pickle
import datetime
import json


# date_time = datetime.datetime.now()
# date = date_time.strftime("%d%m%Y")

# resultJson = { 'HEllo':'hi' }

# with open('data/'+date+'.json', 'w') as fp:
#         json.dump(resultJson, fp)


def Load():
    with open("data/Data.txt", "rb") as pkl_handle:
        output = pickle.load(pkl_handle)
        with open('data/'+'01022023'+'.json', 'w') as fp:
             json.dump(output, fp)

    # with open('data.json', 'w') as fp:
    #     json.dump(resultJson, fp)
Load() 


from requests import put,get
import json
import pandas as pd
import random

headers = {'Content-type': 'application/json'}

#restaurant_data = pd.read_csv("C:/Users/atrivedy/Documents/proj/US.txt",sep="\t")
restaurant_data = pd.read_csv("C:/Users/atrivedy/Documents/Visualilzation/data/store_data.csv",sep="\t")
path_all_us_data = r"C:/Users/atrivedy/Documents/Visualilzation/data/Active_Restaurant_List_05282018.xlsx"
us_restaurant_data = pd.read_excel(path_all_us_data)

def push_all_14084():
    for i in range(500):
        random_error_code = random.randint(1,4)
        nsn = int(us_restaurant_data.iloc[i]['RESTAURANT NUMBER'])
        name = restaurant_data.iloc[restaurant_data['NatlStrNumber'] == (us_restaurant_data.loc[i]['RESTAURANT NUMBER'])]['Region']
        AddressLine = "some address"
        hour = 11
        minute = 10
        time_string = str(hour) + ":" + str(minute)
        data = {
            "nsn": str(nsn),
            "name": str(name),
            "error": str(random_error_code),
            "timestamp": str(time_string),
            "addressline": str(AddressLine),
            "ISO2": "US"
        }
        url = 'http://localhost:9200/stores_ecp/city/' + str(nsn)
        put(url, headers=headers, data=json.dumps(data))

def push_data_to_elastic_search():
    random_index = random.sample(range(1,800), 799) #2499 unique values out of 3000 for US 1024 for rest i.e 3000/2500
    for i in range(0,899):
        random_error_code = random.randint(1,4)
        nsn = int( restaurant_data.iloc[random_index[i]]['NatlStrNumber'] )
        name = restaurant_data.iloc[random_index[i]]['PrimaryCity']
        AddressLine = restaurant_data.iloc[random_index[i]]['Region']

        hour = random.randint(13,14)
        minute = random.randint(0,59)
        time_string = str(hour)+":"+str(minute)

        data = {
            "nsn": str(nsn),
            "name": str(name),
            "error": str(random_error_code),
            "timestamp": str(time_string),
            "addressline": str(AddressLine),
            "ISO2":"US"
        }

        url = 'http://localhost:9200/stores_ecp/city/' + str(nsn)
        put(url, headers=headers, data=json.dumps(data))

def push_SN_data():
    incidents = pd.read_csv('../incident.csv')
    total_inc = incidents.shape[0]
    for i in range(total_inc):
        data = {
            "nsn": str(incidents.iloc[i]["location"]),
            "name": str(incidents.iloc[i]["number"]),
            "error": str(incidents.iloc[i]["priority"]),
            "timestamp": str(incidents.iloc[i]["opened_at"]),
            "addressline": str(restaurant_data["Region"].loc[restaurant_data["NatlStrNumber"]==incidents.iloc[i]["location"]].values[0]),
            "ISO2": "US"
        }

        url = 'http://localhost:9200/stores_ecp/city/' + str(i)
        put(url, headers=headers, data=json.dumps(data))


if __name__ == '__main__':
    push_SN_data()

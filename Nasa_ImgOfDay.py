import json
import requests
import webbrowser
import shutil 

API_KEY = 'W8dmMr6Gm8z5Sh2YeLdv8XTQbAIsK0M4ekFcolv8'

url = 'https://api.nasa.gov/planetary/apod'

url1= 'https://api.nasa.gov/neo/rest/v1/feed'

param_IVL = {
    'api_key':API_KEY,
    'start_date': '2021-12-20',
    'end_date': '2022-12-25', 
}
#get astronomy picture of the day based on param_APOD saved in json file
#and download the image to the current directory
def APOD():
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2022-02-01',
    'end_date': '2023-02-01',
    
}
    year = 22
    url_APOD = 'https://api.nasa.gov/planetary/apod'  
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    #print(json_data)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
        # Data_file.write(json_data)
    # for i in range (4):
    #     f = open('SpaceImages/SpaceImg'+str(i),'ab')
    #     img_url = json_data[i]['hdurl']
    #     # webbrowser.open(img_url)
    #     res = requests.get(img_url, stream = True)
    #     if res.status_code == 200:
    #         shutil.copyfileobj(res.raw, f)
    #         print('Image sucessfully Downloaded: ','SpaceImg'+str(i))
    #     else:
    #         print('Image Couldn\'t be retrieved')
    #     f.close()
    datafile.close()
    year = 21
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2021-02-01',
    'end_date': '2022-02-01',
    
}
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    #print(json_data)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()

    year = 20
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2020-02-01',
    'end_date': '2021-02-01',

    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)

    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()


    year = 19
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2019-02-01',
    'end_date': '2020-02-01',
    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()

    year = 18
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2018-02-01',
    'end_date': '2019-02-01',
    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()

    year = 17
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2017-02-01',
    'end_date': '2018-02-01',
    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()

    year = 16
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2016-02-01',
    'end_date': '2017-02-01',
    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()

    year = 15
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2015-02-01',
    'end_date': '2016-02-01',
    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()

    year = 14
    param_APOD = {
    'api_key':API_KEY,
    'start_date': '2014-02-01',
    'end_date': '2015-02-01',
    }
    response = requests.get(url_APOD,params = param_APOD)
    json_data = json.loads(response.text)
    with open('All_Data/data_APOD'+str(year)+'.json', 'w') as datafile:
        json.dump(json_data, datafile, ensure_ascii=False)
    datafile.close()


def IVL(param_IVL, count,num):
    url_IVL = 'https://images-api.nasa.gov'
    query = {'q': 'Mars View',
    'nasa_id':'',
    'keywords':'Mars',
    'media_type':'image'
                    }
    response = requests.get('https://images-api.nasa.gov/search', params=param_IVL)

    # print(response.json())
    if (response.status_code == 200):
        data = response.json()
    with open('All_Data/data_IVL'+param_IVL['q']+str(num)+'.json', 'w') as datafile:
        json.dump(response.json(), datafile, ensure_ascii=False)
    datafile.close()
    # print(data)
    return count + 1

def earth_image(param_earth,count):
    url_earth = 'https://api.nasa.gov/EPIC/api/natural/images?api_key='+API_KEY
    response = requests.get(url_earth, params=param_earth)
    if (response.status_code == 200):
        data = response.json()
    with open('All_Data/data_earth'+str(count)+'.json', 'w') as datafile:
        json.dump(data, datafile, ensure_ascii=False)
    datafile.close()
    print(data)


def Hubble():
    url_hub = 'hubblesite.org/api/v3/images'

def Exoplant():
    url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"

    # Define the query parameters
    table = "exoplanets"
    select = "*"
    format = "json"

    # Construct the full query URL
    query_url = f"{url}?table={table}&select={select}&format={format}"

    # Send the request and get the response
    response = requests.get(query_url)

    # Parse the response as JSON
    print(response.text)
    json_data = json.loads(response.text)

    # Print the JSON data to the console
    print(json.dumps(json_data, indent=4))

    
def main():

    # APOD()

    count = 0
    query_mars = {'q': 'Mars View',
    'nasa_id':'',
    'title':'Mars View',
    'keywords':'Mars',
    'media_type':'image'
                    }

    count = IVL(query_mars, count)
    query_jupiter = {'q': 'Jupiter View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_jupiter, count)

    query_saturn = {'q': 'Saturn View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_saturn, count)

    query_uranus = {'q': 'Uranus View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_uranus, count)

    query_neptune = {'q': 'Neptune View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_neptune, count)

    query_mercury = {'q': 'Mercury View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'

                    }   
    count = IVL(query_mercury, count)

    query_venus = {'q': 'Venus View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_venus, count)

    query_sun = {'q': 'Sun View',  
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_sun, count)

    query_earth = {'q': 'Earth View',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_earth, count)

    query_blackhole = {'q': 'Black Hole',
    'nasa_id':'',
    'title':'Black Hole',
    'keywords':'Black Hole',
    'media_type':'image'
                    }
    count = IVL(query_blackhole, count)

    query_nebula = {'q': 'Nebula',
    'nasa_id':'',
    'title':'Nebula',
    'keywords':'Nebula',
    'media_type':'image'
                    }
    count = IVL(query_nebula, count)

    query_pillarofcreation = {'q': 'Pillar of Creation',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_pillarofcreation, count)

    query_milkyway = {'q': 'Milky Way galaxy',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_milkyway, count)

    query_andromeda = {'q': 'Andromeda galaxy',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_andromeda, count)

    query_asteroid = {'q': 'Asteroid',
    'nasa_id':'',
    'title':'',
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_asteroid, count)

    query_comet = {'q': 'Comet',
    'nasa_id':'',
    'title':'', 
    'keywords':'',
    'media_type':'image'
                    }
    count = IVL(query_comet, count)

    serch_list = ['stellar', 'star', 'galaxy', 
    'universe', 'planet', 'space', 'astronomy', 
    'cosmos', 'solar system', 'spacecraft','Apollo'
    'Neutron star', 'Quasar', 'Pulsar', 'Supernova',
    'Cosmic microwave background radiation', 'Dark matter',
    'Dark energy', 'Supercluster', 'Galaxy cluster', 'Galaxy group',
    'Big Bang','local group','Cosmic dust','Neutron star','Quasar',
    'Pulasr','Luncher','astronomers'
      ]
    for keyword in serch_list:
        query = {'q': keyword,
        'nasa_id':'',
        'title':'',
        'keywords':'',
        'media_type':'image'
                        }
        count = IVL(query, count)

def test():
    count = 0
    for i in range(1,10):

        query = {'q': 'solar system',
        'nasa_id':'',
        'title':'',
        'keywords':'',
        'media_type':'image',
        'page': i    }
        count = IVL(query, 10,i)
test()



# # Exoplant()
# APOD()
# url = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?&table=exoplanets&format=ipac&where=pl_kepflag=1'
# response = requests.get(url)
# json_data = response.json()
# print(json_data)
# query = {'q': 'news',
#         'nasa_id':'',
#         'title':'',
#         'keywords':'',
#         'media_type':'image',
#         'year_start':'2010',
#         'year_end':'2020',
#         'page': 100
#                         }
# count = IVL(query, 48)

# print(count)
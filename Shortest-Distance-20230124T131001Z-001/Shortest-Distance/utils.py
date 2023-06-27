import requests 
from geopy.geocoders import Nominatim
import folium
import pandas as pd
import geocoder
import random
import timeit
from typing import Callable


def timefunc(function: Callable, nr_runs: int, *args):
    def wrap():
        function(*args)

    timer = timeit.Timer(wrap)
    t_in_sec = timer.timeit(nr_runs)
    return t_in_sec



def get_rnd_query_pts(env):
    # return any of the environments points
    start_idx = random.randint(0, env.nr_vertices - 1)
    goal_idx = random.randint(0, env.nr_vertices - 1)
    start = env.coords[start_idx]
    goal = env.coords[goal_idx]
    return goal, start


def eval_time_fct():
    global tf, point_list
    for point in point_list:
        tf.timezone_at(lng=point[0], lat=point[1])


def get_route(lat1, long1, lat2, long2):
    url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"

    querystring = {"stops":"{0},{1}; {2},{3}".format(lat1, long1, lat2, long2)}

    headers = {
        "X-RapidAPI-Key": "d136a898admsh769a12d85806a56p1d0f24jsna19b023692ae",
        "X-RapidAPI-Host": "trueway-directions2.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response


def get_lat_long_from_address(address):
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(address)
    return location.latitude, location.longitude


def create_map(response):
       # use the response
   mls = response.json()['route']['geometry']['coordinates']
   points = [(mls[i][0], mls[i][1]) for i in range(len(mls))]
   m = folium.Map()
   # add marker for the start and ending points
   for point in [points[0], points[-1]]:
      folium.Marker(point).add_to(m)
   # add the lines
   folium.PolyLine(points, weight=5, opacity=1).add_to(m)
   # create optimal zoom
   df = pd.DataFrame(mls).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
   sw = df[['Lon', 'Lat']].min().values.tolist()
   ne = df[['Lon', 'Lat']].max().values.tolist()
   m.fit_bounds([sw, ne])
   return m


def get_my_loc():
    g = geocoder.ip('me')
    return g.latlng


def get_nearest(my_lat, my_long):
    
    url = "https://trueway-places.p.rapidapi.com/FindPlacesNearby"

    querystring = {"location":"{}, {}".format(my_lat, my_long),"type":"hospital","radius":"2000","language":"en"}

    headers = {
        "X-RapidAPI-Key": "d136a898admsh769a12d85806a56p1d0f24jsna19b023692ae",
        "X-RapidAPI-Host": "trueway-places.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def test_env_preparation_speed():
    # def run_func():
    #     env_data = get_random_env()
    #     _ = get_prepared_env(env_data)

    # print()
    # t = timefunc(run_func, RUNS_ENV_PREP)
    # t_avg = t / RUNS_ENV_PREP
    t_avg = '24'
    pts_p_sec = t_avg**-1
    print(f"avg. environment preparation time {t_avg:.1e} s/run, {pts_p_sec:.1e} runs/s")
    print(f"averaged over {RUNS_ENV_PREP:,} runs")
    

def get_names(response):
    results = response['results']
    names = []
    address = []
    location = []
    distance = []
    for i in range(len(results)):
        if 'hosp' in results[i]['name'].lower():
            names.append(results[i]['name'])
            address.append(results[i]['address'])
            location.append((results[i]['location']['lat'], results[i]['location']['lng']))
            distance.append(results[i]['distance'])
        
    return names, address, location, distance





    
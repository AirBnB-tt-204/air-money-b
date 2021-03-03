"""Prediction of Optimal Price based on Listing Properties"""
from os import path
from sys import maxsize
from csv import DictReader, field_size_limit
from json import dumps

import numpy as np

from tensorflow.keras.models import model_from_json
from joblib import load

Model = None
MMS = None
Encoder = None

Cities = ['Asheville', 'Austin', 'Boston', 'Broward County', 'Cambridge',
        'Chicago', 'Clark County', 'Columbus', 'Denver', 'Hawaii',
        'Jersey City', 'Los Angeles', 'Nashville', 'New Orleans',
        'New York City', 'Oakland', 'Pacific Grove', 'Portland',
        'Rhode Island', 'Salem', 'San Clara Country', 'San Diego',
        'San Francisco', 'San Mateo County', 'Santa Cruz County',
        'Seattle', 'Twin Cities MSA', 'Washington D.C.']

city_neighborhood_lists = None

listing_params = {
    'property_types':['Apartment', 'House', 'Condominium', 'Townhouse', 'Loft'], 
    'room_types':['Entire home/apt', 'Private room', 'Shared room']
    }

def init_city_neighborhood_info():
    global city_neighborhood_lists
    
    city_neighborhood_lists = {}
    
    with open(path.join(path.dirname(__file__), 'city_neighborhood.csv')) as csv_file:
        cities = DictReader(csv_file)
        old_limit = field_size_limit(maxsize)
        
        for city in cities:
            city_neighborhood_lists[city['city']] = list(set(eval(city['neighborhood_list'])))
      
        field_size_limit(old_limit)

    listing_params['cities'] = list(city_neighborhood_lists.keys())
    listing_params['city_neigh'] = dumps(city_neighborhood_lists)

    print(city_neighborhood_lists.keys(), len(city_neighborhood_lists.keys()))
    
    
def init_optimal_price_model():
    # Load Serialized Model to Reuse:
    global Model, MMS, Encoder

    with open(path.join(path.dirname(__file__),'model/nn.json'), 'r') as json_file:
        Model = model_from_json(json_file.read())

    Model.load_weights(path.join(path.dirname(__file__),'model/nn.h5'))
    
    # Load Transformations:
    MMS = load(path.join(path.dirname(__file__),'model/MMS.gz'))
    Encoder = load(path.join(path.dirname(__file__),'model/encoder.gz'))
    

def get_optimal_pricing(**listing):
    global Encoder, MMS, Model
    
    print(listing)

    cat_cols = np.array([[listing['neighborhood'], listing['room_type'], listing['city']]])
    num_cols = np.array([[listing['availability_365'], listing['minimum_nights']]])

    print(f'{cat_cols=} {num_cols=}')
    '''
    s1 = Encoder.transform(cat_cols)

    array_joined = np.append(s1, num_cols, axis=1)

    transformed = MMS.transform(array_joined)

    price = Model.predict(transformed)[0][0]
    '''
    price = 100
    
    return price

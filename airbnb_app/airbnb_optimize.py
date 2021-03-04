"""Prediction of Optimal Price based on Listing Properties"""
from os import path
from sys import maxsize
from csv import DictReader, field_size_limit
from json import dumps

import numpy as np

from tensorflow.keras.models import model_from_json
from joblib import load


class CityNeighborhood():
    
    def __init__(self):
        city_neighborhood_lists = {}

        self.listing_params = {
            'property_types':['Apartment', 'House', 'Condominium', 'Townhouse', 'Loft'], 
            'room_types':['Entire home/apt', 'Private room', 'Shared room']
        }
        
        with open(path.join(path.dirname(__file__), 'city_neighborhood.csv')) as csv_file:
            cities = DictReader(csv_file)
            old_limit = field_size_limit(maxsize)
        
            for city in cities:
                # We convert to set to remove duplicate neighborhood names
                # and back to list to enable conversion to JSON - json.dumps()
                # cannot handle set objects.
                neighs = list(set(eval(city['neighborhood_list'])))
                neighs.sort()
                city_neighborhood_lists[city['city']] = neighs
      
            field_size_limit(old_limit)


        self.listing_params['cities'] = list(city_neighborhood_lists.keys())
    
        #Convert city_neighborhood_lists to JSON for use by Javascript
        self.listing_params['city_neigh'] = dumps(city_neighborhood_lists)

        print(city_neighborhood_lists.keys(), len(city_neighborhood_lists.keys()))

    
class OptimalPriceModel():

    def __init__(self):
        with open(path.join(path.dirname(__file__),'model/nn.json'), 'r') as json_file:
            self.Model = model_from_json(json_file.read())

        self.Model.load_weights(path.join(path.dirname(__file__),'model/nn.h5'))
    
        # Load Transformations:
        self.MMS = load(path.join(path.dirname(__file__),'model/MMS.gz'))
        self.Encoder = load(path.join(path.dirname(__file__),'model/encoder.gz'))
    

    def get_optimal_pricing(self, **listing):
    
        print(listing)

        cat_cols = np.array([[listing['neighborhood'], listing['room_type'], listing['city']]])
        num_cols = np.array([[int(listing['availability_365']), int(listing['minimum_nights'])]])

        print(f'{cat_cols=} {num_cols=}')
    
        s1 = self.Encoder.transform(cat_cols)

        array_joined = np.append(s1, num_cols, axis=1)

        transformed = self.MMS.transform(array_joined)

        prediction = self.Model.predict(transformed)
    
        #SQLAlchemy complains about  type 'numpy.float32'
        #Convert to float
        price = round(prediction[0][0])
    
        return price
    
    
CITY_NEIGHBORHOOD = CityNeighborhood()
OPTIMAL_PRICE_MODEL = OptimalPriceModel()

"""Prediction of Optimal Price based on Listing Properties"""
from os import path
from sys import maxsize
from csv import DictReader, field_size_limit
from json import dumps

import numpy as np

from tensorflow.keras.models import model_from_json
from joblib import load


class ListingParams(dict):
    '''
    This class provides all the parameters required
    for dealing with listings in the edit and add
    listing templates.
    '''
    def __init__(self):
        super().__init__()

        city_neighborhood_lists = {}

        self['property_types'] = ['Apartment', 'House', 'Condominium',
                                  'Townhouse', 'Loft']
        self['room_types'] = ['Entire home/apt', 'Private room', 'Shared room']

        # The city_neighborhood.csv file is generated from the dataset used
        # to generate the model
        # df1 = df.groupby('city').neighbourhood.apply(list).\
        #    reset_index(name='neighborhood_list')
        # df1.to_csv('city_neighborhood.csv')
        with open(path.join(path.dirname(__file__),
                            'city_neighborhood.csv')) as csv_file:
            cities = DictReader(csv_file)
            old_limit = field_size_limit(maxsize)

            for city in cities:
                # We secure the use of eval() by restricting the symbols
                # available, even removing __builtins__.
                # We convert to set to remove duplicate neighborhood names
                # and back to list to enable conversion to JSON - json.dumps()
                # cannot handle set objects.
                neighs = list(set(eval(city['neighborhood_list'],
                                       {'__builtins__': None})))
                neighs.sort()
                city_neighborhood_lists[city['city']] = neighs

            field_size_limit(old_limit)

        self['cities'] = list(city_neighborhood_lists.keys())

        # Convert city_neighborhood_lists to JSON for use by Javascript
        self['city_neigh'] = dumps(city_neighborhood_lists)

        print(city_neighborhood_lists.keys(),
              len(city_neighborhood_lists.keys()))


class OptimalPriceModel():

    '''
    This class encapsulates the predictive model that is used
    to compute the optimal pricing for a listing.
    '''
    def __init__(self):
        with open(path.join(path.dirname(__file__),
                            'model/nn.json'), 'r') as json_file:
            self.model = model_from_json(json_file.read())

        self.model.load_weights(
            path.join(path.dirname(__file__), 'model/nn.h5'))

        # Load Transformations:
        self.min_max_scaler = load(path.join(path.dirname(__file__),
                                             'model/MMS.gz'))
        self.encoder = load(
            path.join(path.dirname(__file__), 'model/encoder.gz'))

    def get_optimal_pricing(self, **listing):

        '''
        Given listing info returns the optimal price.
        '''
        cat_cols = np.array(
            [[listing['neighborhood'], listing['room_type'], listing['city']]])
        num_cols = np.array(
            [[int(listing['availability_365']),
              int(listing['minimum_nights'])]]
        )

        cat_cols_transformed = self.encoder.transform(cat_cols)

        array_joined = np.append(cat_cols_transformed, num_cols, axis=1)

        transformed = self.min_max_scaler.transform(array_joined)

        prediction = self.model.predict(transformed)

        # SQLAlchemy complains about  type 'numpy.float32'
        # Convert to python float with round()
        price = round(prediction[0][0])

        return price


LISTING_PARAMS = ListingParams()
OPTIMAL_PRICE_MODEL = OptimalPriceModel()

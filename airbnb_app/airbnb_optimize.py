"""Prediction of Optimal Price based on Listing Properties"""
import xgboost
from pickle import load
from os import path

PICKLED_MODEL_FILE='xgboost_model.sav'
PICKLED_MODEL_FILEPATH = path.join(path.dirname(__file__), PICKLED_MODEL_FILE)

Model = None

def get_model(force_refresh=False):
    global Model
    
    if force_refresh:
        del Model
        Model = None
        
    if Model is None:
        Model = load(open(PICKLED_MODEL_FILEPATH, 'rb'))
        
    return Model

def get_optimal_pricing(**listing):
    '''
    Just return 100 for now - will call out to a proper predictive model later
    '''
    
    model = get_model()
    
    print(listing, model)

    price = listing.get('price', 0)

    price = price+10 if price else 100

    return price

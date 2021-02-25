"""Prediction of Optimal Price based on Listing Properties"""


def get_optimal_pricing(**listing):
    ''' Just return 100 for now - will call out to a proper predictive model later'''
    print(listing)
    
    price = listing.get('price', 0)
    
    price = price+10 if price else 100
    
    return price
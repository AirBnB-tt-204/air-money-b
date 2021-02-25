from flask import Blueprint, jsonify, request, render_template , flash, redirect
from .models import DB, User, Listing
from .airbnb_optimize import get_optimal_pricing
from os import getenv
from dotenv import load_dotenv

load_dotenv()

airbnb_routes = Blueprint("airbnb_routes", __name__)

@airbnb_routes.route('/')
def default_route():
    return render_template('airbnb_op_layout.html')
    
@airbnb_routes.route("/users")
def list_users():
    # SELECT * FROM users
    users = User.query.all()
    print(users)   

    return render_template("users.html", message="Users and their listings", users=users)

@airbnb_routes.route("/users/add")
def add_user():
    return render_template("add_user.html")

@airbnb_routes.route("/users/create", methods=["POST"])
def create_user():
    
    users = User.query.all()

    name=request.form['name']
    
    #If the user doesn't already exist add to the user table
    print(User.query.filter(User.name == name).first())
    if user := User.query.filter(User.name == name).first() is None:
        # create user based on the username passed into the function
        
        user = User(id=len(users)+1, name=name)
        DB.session.add(user)
        DB.session.commit()
        flash(f"User {user.name} created successfully!", "success")

    
    return redirect(f"/users")

@airbnb_routes.route("/listings/add", methods=["POST"])
def add_listing():
    print(request.form)
    user_id = request.form['user']
    user = User.query.get(user_id)
    return render_template("add_listing.html", user=user)

@airbnb_routes.route("/listings/create", methods=["POST"])
def create_listings():

    new_id = len(Listing.query.all()) + 1

    print(request.form)
    listing = Listing(id=new_id, **request.form, price=get_optimal_pricing(**request.form))
    
    DB.session.add(listing)
    DB.session.commit()
    flash(f"Listing {listing.name} created successfully!", "success")

    
    return redirect(f"/users")

@airbnb_routes.route("/listings/edit", methods=["POST"])
def edit_listing():
    listing_id = request.form['listing']
    print(f'{listing_id=}')
    
    listing = Listing.query.get(listing_id)
    print(listing)
    return render_template("edit_listing.html", listing=listing)

@airbnb_routes.route("/listings/modify", methods=["POST"])
def modify_listings():
    
    print(request.form)

    listing = Listing.query.get(request.form['id'])
    
    print(listing)
    
    for attr in request.form:
        setattr(listing, attr, request.form[attr]) 
    
    listing.price = get_optimal_pricing(**request.form)
    
    print(listing)
    
    
    DB.session.commit()
    flash(f"Listing {listing.name} edited successfully!", "success")

    
    return redirect(f"/users")

@airbnb_routes.route("/listings/delete", methods=["POST"])
def delete_listings():
    Listing.query.filter_by(id=request.form['listing']).delete()
    DB.session.commit()
    return redirect(f"/users")

def get_dict_from_listing(listing):
    attrs = ['location', 'room_type', 'name', 'id', 'price', 'min_nights', 'property_type', 'user_id']
    
    ret = {}
    
    for attr in attrs:
        ret[attr] = getattr(listing, attr)
        
    return ret

@airbnb_routes.route("/listings/update", methods=["POST"])
def update_listings():
    
    listings = Listing.query.all()
    
    for listing in listings:
        listing.price = get_optimal_pricing(**get_dict_from_listing(listing))
        
    DB.session.commit()
    
    return redirect(f"/users")

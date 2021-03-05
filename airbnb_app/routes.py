'''
Flask routes for the airbnb app
'''
from flask import Blueprint, request, render_template, flash, redirect
from .models import DB, User, Listing
from .airbnb_optimize import OPTIMAL_PRICE_MODEL, LISTING_PARAMS

LISTING_ATTRS = ['city', 'neighborhood', 'property_type',
                 'room_type', 'minimum_nights', 'availability_365', 'price']

airbnb_routes = Blueprint("airbnb_routes", __name__)


@airbnb_routes.route('/')
def default_route():
    return render_template('airbnb_op_layout.html')


@airbnb_routes.route("/users")
def list_users():
    # SELECT * FROM users
    users = User.query.all()

    return render_template("users.html", message="Users and their listings",
                           users=users, listing_attrs=LISTING_ATTRS)


@airbnb_routes.route("/users/add")
def add_user():
    return render_template("add_user.html")


@airbnb_routes.route("/users/create", methods=["POST"])
def create_user():

    name = request.form['name']

    # If the user doesn't already exist add to the user table
    if user := User.query.filter(User.name == name).first() is None:
        # create user based on the name passed via request

        user = User(name=name)
        DB.session.add(user)
        DB.session.commit()
        flash(f"User {user.name} created successfully!", "success")

    return redirect("/users")


@airbnb_routes.route("/listings/add", methods=["POST"])
def add_listing():

    user_id = request.form['user']
    user = User.query.get(user_id)

    return render_template("add_listing.html", user=user,
                           **LISTING_PARAMS)


@airbnb_routes.route("/listings/create", methods=["POST"])
def create_listings():

    listing = Listing(
        **request.form,
        price=OPTIMAL_PRICE_MODEL.get_optimal_pricing(**request.form)
    )

    DB.session.add(listing)
    DB.session.commit()
    flash(f"Listing {listing.name} created successfully!", "success")

    return redirect("/users")


@airbnb_routes.route("/listings/edit", methods=["POST"])
def edit_listing():
    listing_id = request.form['listing']

    listing = Listing.query.get(listing_id)

    return render_template("edit_listing.html",
                           listing=listing, **LISTING_PARAMS)


@airbnb_routes.route("/listings/modify", methods=["POST"])
def modify_listings():

    # Get the listing entry/row to be modified
    listing = Listing.query.get(request.form['id'])


    # Update the listing entry/row with new data from request
    for attr in request.form:
        setattr(listing, attr, request.form[attr])

    # Get the (potentially) new optimal listing price
    listing.price = OPTIMAL_PRICE_MODEL.get_optimal_pricing(**request.form)

    # Commit the changes to the DB.
    DB.session.commit()
    flash(f"Listing {listing.name} edited successfully!", "success")

    return redirect("/users")


@airbnb_routes.route("/listings/delete", methods=["POST"])
def delete_listings():
    Listing.query.filter_by(id=request.form['listing']).delete()
    DB.session.commit()
    return redirect("/users")


def get_dict_from_listing(listing):

    ret = {}

    for attr in LISTING_ATTRS:
        ret[attr] = getattr(listing, attr)

    return ret


@airbnb_routes.route("/listings/update", methods=["POST"])
def update_listings():

    listings = Listing.query.all()

    for listing in listings:
        listing.price = OPTIMAL_PRICE_MODEL.get_optimal_pricing(
            **get_dict_from_listing(listing))

    DB.session.commit()

    return redirect("/users")

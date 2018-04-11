from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from forms import DashboardSearchForm, MealInfoForm
from models import db, Meals, Reservations, Users
from flask_googlemaps import Map, icons
from APIs import fetch_postcode
from math import radians, cos, sin, asin, sqrt

meals_blueprint = Blueprint('meals_blueprint', __name__, template_folder='templates')
DEFAULT_DISTANCE_IN_KM = 5


@meals_blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    form = DashboardSearchForm()
    trdmap = None
    is_search = False
    buttons = [
        {'text': 'HOST', 'url': url_for('meals_blueprint.add_meal')},
        {'text': 'SIGN OUT', 'url': url_for('auth_blueprint.logout')}
    ]
    all_meals = []
    postcode = request.args.get('postcode')

    # if form.validate_on_submit():
    if postcode is not None:
        is_search = True
        [status, data] = fetch_postcode(postcode)
        if status == 200:
            searched_lat, searched_lng = data['result']['latitude'], data['result']['longitude']
            lat = searched_lat
            lng = searched_lng
            all_meals = Meals.query.all()

            # add distance between the target meals and searching postcode
            for meal in all_meals:
                meal.distance = _round_float_point(_haversine(meal.lng,
                                                              meal.lat,
                                                              searched_lng,
                                                              searched_lat))
                meal.isReserved = Reservations.query.filter_by(meal_id=meal.id,
                                                               guest_id=current_user.id).first() is not None
                meal.host = Users.query.filter_by(id=meal.user_id).first().username
                meal.rsvp_num = Reservations.query.filter_by(meal_id=meal.id).count()
                meal.isEditable = Meals.query.filter_by(id=meal.id, user_id=current_user.id).first() is not None

            all_meals = list(filter(lambda m: m.distance < DEFAULT_DISTANCE_IN_KM, all_meals))
            markers = [{
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<a style='color:#000' href='{}'><h3>{} hosted by: {}</h3></a>".format(
                    "#meal" + str(m.id),
                    m.name,
                    m.host)
            } for m in all_meals]
            trdmap = Map(
                identifier="trdmap",
                varname="trdmap",
                lat=lat,
                lng=lng,
                markers=markers
            )

    return render_template('dashboard.html',
                           user_id=current_user.id,
                           form=form,
                           meals=all_meals,
                           is_search=is_search,
                           searched_postcode=postcode,
                           trdmap=trdmap,
                           buttons=buttons,
                           url_for_redirect=request.url,
                           url_for_rsvp=url_for('meals_blueprint.rsvp'),
                           url_for_cancel=url_for('meals_blueprint.cancel'),
                           url_for_index=url_for('meals_blueprint.dashboard'),
                           url_for_edit=url_for('meals_blueprint.edit_meal'),
                           url_for_dashboar=url_for('meals_blueprint.dashboard'))


@meals_blueprint.route('/meal/add', methods=['GET', 'POST'])
@login_required
def add_meal():
    form = MealInfoForm()
    if form.validate_on_submit():
        [status, data] = fetch_postcode(form.postcode.data)
        if status == 200:
            # image = form.image.data
            meal = Meals(name=form.name.data,
                         description=form.description.data,
                         postcode=form.postcode.data,
                         guest_num=form.guest_num.data,
                         date=form.date.data,
                         time=form.time.data,
                         price=form.price.data,
                         lat=data['result']['latitude'],
                         lng=data['result']['longitude'],
                         user_id=current_user.id)
            db.session.add(meal)
            db.session.commit()
            return redirect(url_for('meals_blueprint.dashboard'))
        else:
            flash('Please enter a valid postcode.')
    return render_template('add_meal.html', form=form, url_for_index=url_for('meals_blueprint.dashboard'))


@meals_blueprint.route('/meal/edit', methods=['GET', 'POST'])
@login_required
def edit_meal():
    user_id = request.args.get('user_id')

    if str(current_user.id) != user_id:
        return redirect(url_for('meals_blueprint.dashboard'))

    meal_id = request.args.get('meal_id')
    url_for_redirect = request.args.get('redirect')
    meal = Meals.query.filter_by(user_id=user_id, id=meal_id).first()
    form = MealInfoForm()

    if form.validate_on_submit():
        [status, data] = fetch_postcode(form.postcode.data)
        if status == 200:
            meal.name = form.name.data
            meal.description = form.description.data
            meal.postcode = form.postcode.data
            meal.guest_num = form.guest_num.data
            meal.date = form.date.data
            meal.time = form.time.data
            meal.price = form.price.data
            meal.lat = data['result']['latitude']
            meal.lng = data['result']['longitude']
            meal.user_id = current_user.id
            db.session.commit()
            return redirect(url_for_redirect)
        else:
            flash('Please enter a valid postcode.')

    return render_template('edit_meal.html',
                           form=form,
                           meal=meal,
                           url_for_delete="{}?user_id={}&meal_id={}".format(url_for('meals_blueprint.delete_meal'),
                                                                            user_id, meal_id),
                           url_for_index=url_for('meals_blueprint.dashboard'))


@meals_blueprint.route('/meal/delete')
@login_required
def delete_meal():
    user_id = request.args.get('user_id')
    meal_id = request.args.get('meal_id')
    # db.session.deleteAll(Reservations.query.filter_by(meal_id=meal_id).all())
    # TODO: delete all reservation which has meal_id = meal_id
    db.session.delete(Meals.query.filter_by(user_id=user_id, id=meal_id).first())
    db.session.commit()
    return redirect(url_for('meals_blueprint.dashboard'))


@meals_blueprint.route('/reservation/rsvp')
@login_required
def rsvp():
    guest_id = request.args.get('user_id')
    meal_id = request.args.get('meal_id')
    url_for_redirect = request.args.get('redirect')
    db.session.add(Reservations(guest_id=guest_id, meal_id=meal_id))
    db.session.commit()
    return redirect(url_for_redirect)


@meals_blueprint.route('/reservation/cancel')
@login_required
def cancel():
    guest_id = request.args.get('user_id')
    meal_id = request.args.get('meal_id')
    url_for_redirect = request.args.get('redirect')
    db.session.delete(Reservations.query.filter_by(guest_id=guest_id, meal_id=meal_id).first())
    db.session.commit()
    return redirect(url_for_redirect)


def _haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    reference: https://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points#15737218
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km


def _round_float_point(num):
    """Round a float number to two decimal only number"""
    return float(str(round(num, 2)))

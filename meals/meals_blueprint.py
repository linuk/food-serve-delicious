from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from forms import DashboardSearchForm, MealInfoForm
from models import db, Meals, Reservations
from flask_googlemaps import Map, icons
from APIs import fetch_postcode

meals_blueprint = Blueprint('meals_blueprint', __name__, template_folder='templates')


@meals_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardSearchForm()
    meals = []
    trdmap = None
    is_search = postcode = False
    buttons = [
        {'text': 'HOST', 'url': url_for('meals_blueprint.add_meal')},
        {'text': 'SIGN OUT', 'url': url_for('auth_blueprint.logout')}
    ]

    if form.validate_on_submit():
        is_search = True
        postcode = form.postcode.data
        meals = Meals.query.filter_by(postcode=postcode).all()
        [status, data] = fetch_postcode(postcode)

        if status == 200:
            lat = data['result']['latitude']
            lng = data['result']['longitude']
            all_meals = []
            trdmap = Map(
                identifier="trdmap",
                varname="trdmap",
                cluster=True,
                cluster_gridsize=10,
                lat=lat,
                lng=lng,
                markers=[
                    {
                        'lat': m.lat,
                        'lng': m.lng,
                        'infobox': "<a href='%s'><h3>%s hosted by: %s</h3></a>"
                            .format(url_for('meal_blueprint.details'),
                                    m.name,
                                    m.Users.query.filter_by(id=m.user_id).first().username)
                    } for m in all_meals
                ]
            )

    return render_template('dashboard.html',
                           form=form,
                           meals=meals,
                           is_search=is_search,
                           searched_postcode=postcode,
                           trdmap=trdmap,
                           buttons=buttons)


@meals_blueprint.route('/meal/details')
@login_required
def details():
    return render_template('details.html')


@meals_blueprint.route('/meal/add', methods=['GET', 'POST'])
@login_required
def add_meal():
    print('add')
    form = MealInfoForm()
    if form.validate_on_submit():
        print('pass')
        [status, data] = fetch_postcode(form.postcode.data)
        print(status)
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
            # TODO: Flash this error message.
    return render_template('add_meal.html', form=form)


@meals_blueprint.route('/meal/edit')
@login_required
def edit_meal():
    return render_template('edit_meal.html')

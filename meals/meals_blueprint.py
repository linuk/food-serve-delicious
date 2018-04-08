from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required
from forms import DashboardSearchForm
from models import Meals, Reservations
from flask_googlemaps import GoogleMaps
from credientials import GOOGLE_MAP_API_KEY
meals_blueprint = Blueprint('meals_blueprint', __name__, template_folder='templates')


@meals_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardSearchForm()
    meals = []
    is_search = postcode = False
    if form.validate_on_submit():
        is_search = True
        postcode = form.postcode.data
        meals = Meals.query.filter_by(postcode=postcode).all()
    return render_template('dashboard.html', form=form, meals=meals, is_search=is_search, searched_postcode=postcode)


@meals_blueprint.route('/meal/add')
@login_required
def add_meal():
    return render_template('add_meal.html')


@meals_blueprint.route('/meal/edit')
@login_required
def edit_meal():
    return render_template('edit_meal.html')

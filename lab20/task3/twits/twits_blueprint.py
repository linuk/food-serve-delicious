from flask import Blueprint, redirect, url_for, render_template
from models import db, Twits, Users
from forms import twitForm
from flask_login import login_required, current_user

twits_blueprint = Blueprint('twits_blueprint', __name__, template_folder='templates')


@twits_blueprint.route('/edit')
@twits_blueprint.route('/edit/<twit_id>', methods=['GET', 'POST'])
@login_required
def edit_twit(twit_id):
    if twit_id is None:
        return redirect(url_for('twits_blueprint.index'))
    else:
        form = twitForm()
        if form.validate_on_submit():
            twit = Twits.query.filter_by(twit_id=twit_id).first()
            twit.twit = form.twit.data
            db.session.commit()
            return redirect(url_for('twits_blueprint.dashboard'))

        twit = Twits.query.filter_by(twit_id=twit_id).first()
        return render_template('edit_twit.html', form=form, value=twit.twit)


@twits_blueprint.route('/delete')
@twits_blueprint.route('/delete/<twit_id>', methods=['GET', 'POST'])
@login_required
def delete_twit(twit_id):
    if twit_id is None:
        return redirect(url_for('twits_blueprint.index'))
    else:
        db.session.delete(Twits.query.filter_by(twit_id=twit_id).first())
        db.session.commit()
        return redirect(url_for('twits_blueprint.dashboard'))


@twits_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = twitForm()
    user_id = current_user.user_id
    if form.validate_on_submit():
        twit = Twits(twit=form.twit.data, user_id=user_id)
        db.session.add(twit)
        db.session.commit()

    message = ''
    button_logout = {'url': url_for('login_blueprint.logout'), 'text': 'Logout'}
    buttons = [button_logout]
    twits = Users.query.filter_by(user_id=user_id).first().twits
    return render_template('index.html', message=message, page_title='Dashboard', buttons=buttons, twits=twits,
                           isLogin=True, form=form, url_to_edit_twit=url_for('twits_blueprint.edit_twit'),
                           url_to_delete_twit=url_for('twits_blueprint.delete_twit'))


@twits_blueprint.route('/', methods=['GET', 'POST'])
def index():
    message = 'You are not logged in.'
    buttons = [
        {'url': url_for('login_blueprint.signUp'), 'text': 'Sign Up'},
        {'url': url_for('login_blueprint.login'), 'text': 'Login'}
    ]
    form = url_to_edit_twit = url_to_delete_twit = None
    return render_template('index.html', message=message, page_title='Twits', buttons=buttons, twits=[],
                           isLogin=False, form=form, url_to_edit_twit=url_to_edit_twit,
                           url_to_delete_twit=url_to_delete_twit)

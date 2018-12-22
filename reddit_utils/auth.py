
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .reddit import get_reddit_object

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':

        error = None

        token = {}
        token['client_id'] = request.form['clientid']
        token['client_secret'] = request.form['clientsecret']
        token['username'] = request.form['username']
        token['password'] = request.form['password']

        result = get_reddit_object(token)

        if result['status'] == 'error':
            error = result['data']

        if error is None:
            session.clear()
            session['token'] = token
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth.htm.j2')



@bp.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('auth.login'))



@bp.before_app_request
def load_logged_in_user():

    g.token = session.get('token')



def api_access_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.token is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

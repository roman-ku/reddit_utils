
import logging
import pprint

from flask import (
    Blueprint, flash, g, render_template, request
)

from ..auth import api_access_required
from .search_helpers import perform_search, check_form

bp = Blueprint('search_saved', __name__)

logger = logging.getLogger('logger')



@bp.route('/search_saved', methods=('GET', 'POST'))
@api_access_required
def main():

    logger.debug('%s', pprint.pformat(request.form))

    error = None
    search_results = []

    if request.method == 'POST' and request.form.get('search_term'):

        search_options = check_form(request.form)
        results = perform_search(search_options, g.token)

        if results['status'] == 'success':
            search_results = results['data']
        else:
            error = results['data']

        if error:
            flash(error)

    return render_template('features/search_saved.htm.j2', search_results=search_results)


import operator
import logging
import pprint
from pprint import pprint as pp

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from ..auth import api_access_required
from ..reddit import get_reddit_object
from .search import perform_search, check_form

bp = Blueprint('list_subreddits', __name__)

logger = logging.getLogger('logger')



@bp.route('/list_subreddits', methods=('GET', 'POST'))
@api_access_required
def main():

    logger.debug('%s', pprint.pformat(request.form))

    error = None
    subs = []

    if request.method == 'POST':

        options = check_form(request.form)
        results = get_subs(g.token, **options)

        if results['status'] == 'success':
            subs = results['data']
        else:
            error = results['data']

        if error:
            flash(error)

    return render_template('features/list_subreddits.htm.j2', subs=subs)



def get_subs(token, get_latest, sort_by, sort_reverse):

    result = get_reddit_object(token)

    if result['status'] == 'error':
        return result
    else:
        reddit = result['data']

    results = []

    print('fetching items: ')
    print('-'*200)

    for subreddit in reddit.user.subreddits(limit=None):

        subreddit.id            # trigger loading
        item = vars(subreddit)  # pull off properties

        # get the latest post

        item['latest_post'] = {}

        if get_latest:

            submissions = list(reddit.subreddit(subreddit.display_name).new(limit=1))

            if len(submissions) == 1:
                item['latest_post']['title'] = submissions[0].title
                item['latest_post']['link'] = 'https://reddit.com' + submissions[0].permalink
                item['latest_post']['created_utc'] = submissions[0].created_utc


        results.append(item)

        if sort_by == 'subscribers':
            results.sort(key=operator.itemgetter('subscribers'), reverse=sort_reverse)
        elif sort_by == 'creation_time':
            results.sort(key=operator.itemgetter('created_utc'), reverse=sort_reverse)
        elif sort_by == 'last_post':
            sort_reverse = not sort_reverse
            results = sorted(results, key=lambda d: d.get('latest_post').get('created_utc'), reverse=sort_reverse)

        # pp(item)
        # break

    return {'status': 'success', 'data': results}



def check_form(form):

    ''' Checks the form submitted by the user
        1. Parse the form
        2. Give default values to search options not found in the form
    '''

    logger.debug('Checking request form')

    options = {}

    options['get_latest'] = 'get_latest_post' in form

    if 'sort_by' in form and form['sort_by'] in ['subscribers', 'creation_time', 'last_post']:
        options['sort_by'] = form['sort_by']
    else:
        options['sort_by'] = 'subscribers'

    if 'sort_order' in form and form['sort_order'] == 'desc':
        options['sort_reverse'] = True
    else:
        options['sort_reverse'] = False

    # if we are not getting the latest post, we can't sort by the time of the last post
    if not options['get_latest'] and form['sort_by'] == 'last_post':
        options['sort_by'] = 'subscribers'

    # it makes more sense this way based on how epoch works
    if options['sort_by'] in ['creation_time', 'last_post']:
        options['sort_reverse'] = not options['sort_reverse']

    return options

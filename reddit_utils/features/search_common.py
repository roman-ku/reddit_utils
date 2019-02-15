
import logging

import pprint
from pprint import pprint as pp

from praw.models import Submission
from praw.models import Comment

from flask import (
    flash, g, request
)

from ..reddit import get_reddit_object

logger = logging.getLogger('logger')



def search_page():

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

    return search_results



def perform_search(search_options, token):

    result = get_reddit_object(token)

    if result['status'] == 'error':
        return result

    reddit = result['data']

    results = user_saved(reddit, **search_options)
    results = list(results) if results else []

    return {'status': 'success', 'data': results}



def check_form(form):

    ''' Checks the form submitted by the user
        1. Parse the form
        2. Give default values to search options not found in the form
        3. Clean up items (e.g. make subreddit names all lowercase)
    '''

    logger.debug('Checking request form')

    search_options = {}

    # determine search type
    if 'search_type' in form:
        search_options['search_type'] = form['search_type']
    else:
        search_options['search_type'] = ''

    # determine search terms
    if 'search_term' in form:
        search_options['search_queries'] = [form['search_term']]
    else:
        search_options['search_queries'] = []

    # determine subreddit critera
    if 'subreddits' in search_options:
        search_options['subreddits'] = form['subreddits']
    else:
        search_options['subreddits'] = ['android', 'news', 'WORLDNEWS']
        search_options['subreddits'] = []

    # convert items to lower case
    search_options['subreddits'] = [s.lower() for s in search_options['subreddits']]
    search_options['search_queries'] = [s.lower() for s in search_options['search_queries']]

    return search_options



def user_saved(reddit, **search_options):

    matched = False

    if 'search_type' in search_options and search_options['search_type'] == 'saved_posts':
        source = reddit.user.me().saved(limit=None)
    else:
        source = reddit.user.me().new(limit=None)

    for saved_item in source:

        # we can have two types of objects here:
        # 1. praw.models.reddit.comment.Comment
        # 2. praw.models.reddit.submission.Submission


        # 1. DATA MASSAGING

        saved_item.id            # trigger loading
        item = vars(saved_item)  # pull off properties

        # determine item type
        if isinstance(saved_item, Submission):
            item['type'] = 'submission'
        elif isinstance(saved_item, Comment):
            item['type'] = 'comment'
        else:
            logger.error('Unexpected item type: %s', type(saved_item))


        # 2. PERFORMING SEARCH

        # if we have a "subreddits" critera, check if the item passes the criteria
        if search_options['subreddits'] and not item_in_subreddit(item, search_options['subreddits']):
            continue

        # search through the text items
        for text_key in ['link_title', 'link_permalink', 'link_url', 'selftext', 'title', 'body', 'permalink', 'url']:

            if text_key not in item:
                continue

            if query_in_str(search_options['search_queries'], item[text_key]):
                matched = True
                break

        if matched:
            yield item

        matched = False


    # dump items to file (for development/debugging)
    # for i, saved_item in enumerate(results):
    #     with open('results/' + str(i) + '.txt', 'w', encoding='utf-8') as f:
    #         f.write(pprint.pformat(vars(saved_item), indent=4))



def query_in_str(queries, string):

    ''' Are any of the search queries found in the string
    '''

    string = string.lower()

    for query in queries:
        if query in string:
            return True

    return False



def item_in_subreddit(item, subreddits):

    ''' Does the reddit Submission or Comment belong to one of the subreddits
        to which the user is searching in
    '''

    subreddit = str(item['subreddit']).lower()

    return subreddit in subreddits

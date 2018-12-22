
import logging

import praw
from prawcore.exceptions import OAuthException, ResponseException

logger = logging.getLogger('logger')



def get_reddit_object(token):

    try:

        reddit = praw.Reddit(user_agent='reddit_utils web app by Roman Kuleshov',
                             client_id=token['client_id'],
                             client_secret=token['client_secret'],
                             username=token['username'],
                             password=token['password'])

        reddit.user.me()

        return {'status': 'success', 'data': reddit}

    except OAuthException as err:
        return {'status': 'error', 'data': 'Error: Unable to get API access, please make sure API credentials are correct and try again (check the username and password first)'}

    except ResponseException as err:
        return {'status': 'error', 'data': 'Error: ResponseException: ' + str(err)}

    except Exception as err:
        return {'status': 'error', 'data': 'Unexpected Error: ' + str(err)}

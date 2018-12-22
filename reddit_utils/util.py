
import logging
import os
import pathlib

import arrow



class MakeFileHandler(logging.FileHandler):

	# https://stackoverflow.com/questions/20666764/python-logging-how-to-ensure-logfile-directory-is-created
	# https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python/600612#600612

    def __init__(self, filename, mode='a', encoding=None, delay=0):            
        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)



def format_full_date(value):

    return arrow.get(value).to('US/Pacific').format('ddd  MMM D YYYY  h:mm A') + '  PST'



def format_timestamp(value, only_distance=False):
    
    return arrow.get(value).humanize(only_distance=only_distance)



def format_karma_score(karma):

	if karma > 1000:
		karma = karma / 1000
		karma = str(int(karma)) + 'k'

	return karma

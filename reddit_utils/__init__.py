
import os
import logging
import logging.config

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap

import yaml



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    Bootstrap(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    LOGGER_CONFIG = os.path.join(app.root_path, 'files', 'logging_config.yaml')

    with open(LOGGER_CONFIG) as fid:

        try:
            global_config = yaml.safe_load(fid)
            logging.config.dictConfig(global_config)

        except yaml.YAMLError as exc:
            print(exc)
            logging.basicConfig(level=logging.INFO)


    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    from . import auth
    app.register_blueprint(auth.bp)

    from .features import search_saved
    app.register_blueprint(search_saved.bp)

    from .features import list_subreddits
    app.register_blueprint(list_subreddits.bp)

    @app.route('/')
    def index():
        return redirect(url_for('search_saved.main'))

    from . import util
    app.jinja_env.filters['timestamp'] = util.format_timestamp
    app.jinja_env.filters['full_date'] = util.format_full_date
    app.jinja_env.filters['karma'] = util.format_karma_score

    logger = logging.getLogger('logger')
    logger.info('Testing info logging')
    logger.error('Testing error logging')
    logger.warning('Testing warning logging')

    return app

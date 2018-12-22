
# reddit_utils

A collection of reddit utility scripts organized as a self-hosted web app. Currently the following features are available:

* Search through your saved posts
* Ability to fetch your subreddits

<img src="https://i.imgur.com/6Z3XtYC.png" width="909">

## Install Process

1. Clone the repository to your local machine
1. Make sure Python 3.5+ is installed
1. Build a `.whl` (wheel) file
1. Set up a virtual environment
1. Install the `.whl` file
1. Run the flask app 
1. Open [http://localhost:5000](http://localhost:5000) in browser

[Full instructions can be found here](http://flask.pocoo.org/docs/1.0/tutorial/deploy/#build-and-install)

Note: This web app is meant to be self-hosted on something like a [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi)

## Development Process

This web app is built on [Flask](http://flask.pocoo.org/) + [Bootstrap 4](http://getbootstrap.com/) + [PRAW](https://github.com/praw-dev/praw)

Here are the general instructions:

1. Create a virtual environment
1. Make changes to code
1. Run the flask app

The specific instructions for power shell on Windows:

1. `virtualenv env`
1. `./env/Scripts/activate`
1. `python -m pip install -e .`
1. `$env:FLASK_ENV = "development"`
1. `$env:FLASK_APP = "reddit_utils"`
1. `flask run`

Here are some helpful links that provide more detail:

* https://virtualenv.pypa.io/en/stable/userguide/
* http://flask.pocoo.org/docs/1.0/tutorial/factory/#run-the-application
* http://flask.pocoo.org/docs/1.0/tutorial/install/#install-the-project

## Contributions

Contributions to this project are welcome. If you contribute to the project, your name will appear on the about page.

Helped wanted with the following:

* Change login procedure to use [web app](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#web-application) procedure instead of the [script procedure](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application)
* Add HTTPS support
* Loading indicator
* Persist saved posts for faster searching
* Ability to have multiple search terms (underlying code is there but needs GUI)
* Ability to restrict search by subreddit (underlying code is there but needs GUI)
* Ability to search your own submissions
* Ability to search past the 1000 item limit
* Ability to unhide all your posts
* Ability to export your saved posts in various formats
* For really long comments (only show the first few paragraphs or so, collapse the rest)
* Highlight search terms in results (something like [this](https://markjs.io/))

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Disclaimer

The developer (Roman Kuleshov) of this application (reddit_utils) has no affiliation with reddit inc.

import os
from flask import Flask


# Application Factory
def create_app(test_config=None):

    # Create the app
    app = Flask(__name__, instance_relative_config=True)
    # ToDo: Update Secret Key on Deploy
    app.config.from_mapping(SECRET_KEY='dev')

    # Loads the instance config, if it exists, when not testing
    if test_config is None:

        app.config.from_pyfile('config.py', silent=True)

    else:

        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:

        os.makedirs(app.instance_path)

    except OSError:

        pass

    # Initial Route Page
    @app.route('/test')
    def test():

        return 'TEST: HueScoreAlerts'

    # app_config Import
    from . import app_config

    # dashboard Import
    from . import dashboard
    app.register_blueprint(dashboard.bp)

    # hue Import
    from . import hue
    app.register_blueprint(hue.bp)

    # nfl Import
    from . import nfl
    app.register_blueprint(nfl.bp)

    # nhl Import
    from . import nhl
    app.register_blueprint(nhl.bp)

    # Initiates Application
    return app

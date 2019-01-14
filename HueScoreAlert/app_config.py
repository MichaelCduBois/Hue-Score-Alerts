from flask import current_app, json


def get():

    with current_app.open_resource('app_config.json') as config_file:

        configuration = json.load(config_file)

    return configuration

from flask import current_app, json


def get():

    with current_app.open_resource('app_config.json') as config_file:

        conf = json.load(config_file)

    return conf


def save(key, value):

    config_json = get()

    config_json[key] = value

    with open("HueScoreAlert/app_config.json", "w") as config_file:

        json.dump(config_json, config_file, indent=4)

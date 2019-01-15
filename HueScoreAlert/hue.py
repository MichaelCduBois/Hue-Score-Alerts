from flask import Blueprint, json, redirect, render_template, url_for
from HueScoreAlert import app_config
import urllib.request as api

# Creates Blueprint
bp = Blueprint('hue', __name__, url_prefix='/hue')


# Initial Route Page
@bp.route('/test')
def hello():

    return 'TEST: Hue'


def create_user():

    configuration = app_config.get()

    url = "http://" + configuration["bridge_ip"] + "/api"

    json_data = {"devicetype": configuration["hue_device_name"]}

    params = json.dumps(json_data).encode('utf8')

    req = api.Request(url, data=params, method="POST")

    response = api.urlopen(req).read().decode()

    status = json.loads(response)[0]

    if "success" in status:

        return str(status["success"]["username"])

    elif "error" in status:

        return str(status["error"]["description"])


def get_info(selection):

    configuration = app_config.get()

    json_list = []

    url = "http://" + configuration["bridge_ip"] + "/api/" + configuration["user_token"] + "/" + selection

    response_json = json.loads(api.urlopen(url).read().decode())

    for item in response_json:

        return_json = {"id": item, "name": response_json[item]["name"]}

        json_list.append(return_json)

    return json_list

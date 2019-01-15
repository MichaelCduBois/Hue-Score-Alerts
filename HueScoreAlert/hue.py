from flask import Blueprint, json, redirect, render_template, url_for
from HueScoreAlert import app_config
from time import sleep
import urllib.request as api

# Creates Blueprint
bp = Blueprint('hue', __name__, url_prefix='/hue')


# Initial Route Page
@bp.route('/test')
def hello():

    return 'TEST: Hue'


def create_user():

    conf = app_config.get()

    url = "http://" + conf["bridge_ip"] + "/api"

    json_data = {"devicetype": conf["hue_device_name"]}

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


def get_state(sport):

    conf = app_config.get()

    alert_type, alert_id = conf[sport + "_alert_selection_type"], conf[sport + "_alert_selection_id"]

    url = "http://" + conf["bridge_ip"] + "/api/" + conf["user_token"] + "/" + alert_type + "/" + alert_id

    response_json = json.loads(api.urlopen(url).read().decode())

    hue_state = response_json["state"] if conf[sport + "_alert_selection_type"] == "lights" else response_json["action"]

    current_state = {"on": hue_state["on"], "sat": hue_state["sat"], "bri": hue_state["bri"], "hue": hue_state["hue"]}

    return current_state


def trigger(sport):

    original_state = get_state(sport)

    conf = app_config.get()

    # FixMe - This is PoC. Need to pull from app_config.json instead

    ending = "state" if conf[sport + "_alert_selection_type"] == "lights" else "action"

    url = "http://" + conf["bridge_ip"] + "/api/" + conf["user_token"] + "/" +\
          conf[sport + "_alert_selection_type"] + "/" + conf[sport + "_alert_selection_id"] + "/" + ending

    json_data = {"on": True, "sat": 254, "bri": 254, "hue": 4080, "alert": "select"}

    params = json.dumps(json_data).encode("utf-8")

    request = api.Request(url, data=params, headers=conf["headers"], method="PUT")

    flash = 0

    while flash != 3:

        api.urlopen(request)

        sleep(1.25)

        flash += 1

    # FixMe - This is end of PoC

    # Returns to previous state
    params = json.dumps(original_state).encode("utf-8")

    request = api.Request(url, data=params, headers=conf["headers"], method="PUT")

    api.urlopen(request)

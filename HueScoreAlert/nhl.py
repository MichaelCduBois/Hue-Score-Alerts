from flask import Blueprint, json, redirect, render_template, url_for
from HueScoreAlert import app_config
from urllib.request import urlopen as api_call

# Creates Blueprint
bp = Blueprint('nhl', __name__, url_prefix='/nhl')


# Initial Route Page
@bp.route('/hello')
def hello():

    return 'Hello NHL World!'


# Get NHL Teams
def get_teams():

    configuration = app_config.get()

    response = api_call(configuration["nhl_url"] + "teams")

    team_json = json.loads(response.read().decode())

    teams_list = []

    for team in team_json["teams"]:

        json_team = {"id": str(team["id"]), "name": team["name"]}

        teams_list.append(json_team)

    return teams_list

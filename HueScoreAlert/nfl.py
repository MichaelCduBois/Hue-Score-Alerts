from flask import Blueprint, json, redirect, render_template, url_for
from HueScoreAlert import app_config
from urllib.request import urlopen as api_call

# Creates Blueprint
bp = Blueprint('nfl', __name__, url_prefix='/nfl')


# Initial Route Page
@bp.route('/hello')
def hello():

    return 'Hello NFL World!'


# Get NFL Teams
def get_teams():

    configuration = app_config.get()

    response = api_call(configuration["nfl_url"] + "teams.json")

    team_json = json.loads(response.read().decode())

    teams_list = []

    for team in team_json["teams"]:

        json_team = {"abbr": str(team["abbr"]), "name": team["fullName"]}

        teams_list.append(json_team)

    return teams_list

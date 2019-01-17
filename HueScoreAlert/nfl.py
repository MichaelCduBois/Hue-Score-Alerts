from flask import Blueprint, json, Markup, redirect, render_template, request, url_for
from HueScoreAlert import app_config, hue
import urllib.request as api

# Creates Blueprint
bp = Blueprint('nfl', __name__, url_prefix='/nfl')


# Initial Route Page
@bp.route('/test')
def test():

    return 'TEST: NFL'


# Get NFL Teams
def get_teams():

    conf = app_config.get()

    response = api.urlopen(conf["nfl_url"] + "teams.json")

    team_json = json.loads(response.read().decode())

    teams_list = []

    for team in team_json["teams"]:

        json_team = {"abbr": str(team["abbr"]), "name": team["fullName"]}

        teams_list.append(json_team)

    return teams_list


# NFL HTML Generation
def get_html():

    return Markup(render_template('packages/nfl.html',
                                  nfl_teams=get_teams(),
                                  lights=hue.get_info("lights"),
                                  groups=hue.get_info("groups")))


# Saves NFL Selections
@bp.route('/save', methods=['POST'])
def save_selections():

    # NFL Team Selection
    app_config.save("nfl_team_id", request.form["nfl_selection"].split(':')[0])
    app_config.save("nfl_team_name", request.form["nfl_selection"].split(':')[1])

    # NFL Alert Selection
    app_config.save("nfl_alert_selection_type", request.form["lights_selection"].split(':')[0])
    app_config.save("nfl_alert_selection_id", request.form["lights_selection"].split(':')[1])
    app_config.save("nfl_alert_selection_name", request.form["lights_selection"].split(':')[2])

    # NFL Alert Settings
    app_config.save("nfl_alert_cycles", "none")
    app_config.save("nfl_alert_color", "No Color Selected")
    app_config.save("nfl_alert_style", "No Style Selected")

    return redirect(url_for("dashboard.index"))

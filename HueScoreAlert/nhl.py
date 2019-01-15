from flask import Blueprint, json, Markup, redirect, render_template, request, url_for
from HueScoreAlert import app_config, hue
import urllib.request as api

# Creates Blueprint
bp = Blueprint('nhl', __name__, url_prefix='/nhl')


# Initial Route Page
@bp.route('/test')
def test():

    return 'TEST: NHL'


# Get NHL Teams
def get_teams():

    configuration = app_config.get()

    response = api.urlopen(configuration["nhl_url"] + "teams")

    team_json = json.loads(response.read().decode())

    teams_list = []

    for team in team_json["teams"]:

        json_team = {"id": str(team["id"]), "name": team["name"]}

        teams_list.append(json_team)

    return teams_list


# NHL HTML Generation
def get_html():

    return Markup(render_template('packages/nhl.html',
                                  nhl_teams=get_teams(),
                                  lights=hue.get_info("lights"),
                                  groups=hue.get_info("groups")))


# Saves NHL Selections
@bp.route('/save', methods=['POST'])
def save_selections():

    # NHL Team Selection
    app_config.save("nhl_team_id", request.form["nhl_selection"].split(':')[0])
    app_config.save("nhl_team_name", request.form["nhl_selection"].split(':')[1])

    # NHL Alert Selection
    app_config.save("nhl_alert_selection_type", request.form["lights_selection"].split(':')[0])
    app_config.save("nhl_alert_selection_id", request.form["lights_selection"].split(':')[1])
    app_config.save("nhl_alert_selection_name", request.form["lights_selection"].split(':')[2])

    # TBD
    app_config.save("nhl_alert_cycles", "none")
    app_config.save("nhl_alert_color", "No Color Selected")
    app_config.save("nhl_alert_style", "No Style Selected")

    return redirect(url_for("dashboard.index"))

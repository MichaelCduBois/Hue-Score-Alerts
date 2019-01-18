from celery.app.control import Control
from datetime import datetime
from flask import Blueprint, Flask, json, Markup, redirect, render_template, request, url_for
from HueScoreAlert import app_config, hue, tasks
from time import sleep
import urllib.request as api

# Creates Blueprint
bp = Blueprint('nhl', __name__, url_prefix='/nhl')

# Setup Celery
flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://localhost//',
    CELERY_RESULT_BACKEND='amqp://localhost//'
)
nhl = tasks.make_celery(flask_app)


# Get NHL Teams
def get_teams():

    conf = app_config.get()

    response = api.urlopen(conf["nhl_url"] + "teams")

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
                                  groups=hue.get_info("groups"),
                                  colors=hue.get_colors()))


# Saves NHL Selections
@bp.route('/save', methods=['POST'])
def save_selections():

    config = app_config.get()

    # Stop Celery Worker
    if config["nhl_task_id"] != "none":

        task_id = config["nhl_task_id"]

        Control(nhl).revoke(task_id, terminate=True, signal='SIGKILL')

    # NHL Team Selection
    app_config.save("nhl_team_id", request.form["nhl_selection"].split(':')[0])
    app_config.save("nhl_team_name", request.form["nhl_selection"].split(':')[1])

    # NHL Alert Selection
    app_config.save("nhl_alert_selection_type", request.form["lights_selection"].split(':')[0])
    app_config.save("nhl_alert_selection_id", request.form["lights_selection"].split(':')[1])
    app_config.save("nhl_alert_selection_name", request.form["lights_selection"].split(':')[2])

    # NHL Alert Settings
    app_config.save("nhl_alert_cycles", 3)

    # Alert Color Settings
    if request.form["color_selection"] == "none":

        app_config.save("nhl_alert_color", "No Color Selected")
        app_config.save("nhl_alert_style", "No Style Selected")

    elif request.form["color_selection"] == 'Custom':

        app_config.save("nhl_alert_color", "Custom")
        app_config.save("nhl_alert_style", json.loads(request.form["custom_alert"]))

    else:

        app_config.save("nhl_alert_color", request.form["color_selection"])

        colors = hue.get_colors()

        for color in colors:

            if color["name"] == request.form["color_selection"]:

                app_config.save("nhl_alert_style", color["json"])

    config = app_config.get()

    # Start Celery Worker
    if config["nhl_team_id"] != "none":

        print("Executing Celery Command")

        start.delay()

    return redirect(url_for("dashboard.index"))


def next_game_details():

    conf = app_config.get()

    api_call = api.urlopen(conf["nhl_url"] + "teams/" + conf["nhl_team_id"] + "?expand=team.schedule.next")

    call_data = json.loads(api_call.read().decode())

    game_data = call_data["teams"][0]["nextGameSchedule"]["dates"][0]["games"][0]

    game_pk = str(game_data["gamePk"])

    game_date = str(game_data["gameDate"]).split("Z")[0].replace("T", " ")

    team = "home" if str(game_data["teams"]["home"]["team"]["id"]) == conf["nhl_team_id"] else "away"

    return game_pk, game_date, team


def time_to_game(game_date):

    now = str(datetime.utcnow().isoformat()).split(".")[0].replace("T", " ")

    current_time = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

    game_start = datetime.strptime(game_date, "%Y-%m-%d %H:%M:%S")

    time_difference = game_start - current_time

    sleep_duration = int(time_difference.total_seconds())

    while sleep_duration > 0:

        print("Seconds to game: " + str(sleep_duration))

        sleep(1)

        sleep_duration -= 1


def game_details(game_pk, team):

    conf = app_config.get()

    api_call = api.urlopen(conf["nhl_url"] + "game/" + game_pk + "/feed/live")

    call_data = json.loads(api_call.read().decode())

    current_score = call_data["liveData"]["linescore"]["teams"][team]["goals"]

    game_status = call_data["gameData"]["status"]["detailedState"]

    return current_score, game_status


@nhl.task()
def start():

    app_config.save("nhl_task_id", start.request.id)

    game_pk, game_date, team = next_game_details()

    time_to_game(game_date)

    current_score, game_status = game_details(game_pk, team)

    while game_status != "Final":

        new_score, game_status = game_details(game_pk, team)

        if new_score > current_score:

            print("GOAL: " + str(new_score))

            hue.trigger("nhl")

            current_score = new_score

    print("The game status is: " + game_status)

    sleep(60)

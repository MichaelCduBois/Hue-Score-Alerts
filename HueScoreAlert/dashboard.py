from flask import Blueprint, Markup, redirect, render_template, request, send_file, url_for
from HueScoreAlert import app_config, hue, nhl, nfl

# Creates Blueprint
bp = Blueprint('dashboard', __name__)


# Index Setup
@bp.route('/')
def index():

    configuration = app_config.get()

    if configuration["bridge_ip"] == "XXX.XXX.XXX.XXX":

        return render_template('index.html',
                               selections=app_config.get(),
                               dashboard_html=None,
                               nhl_html=None,
                               nfl_html=None,
                               config_html=Markup(render_template('packages/app_config.html',
                                                                  selections=app_config.get())))

    else:

        return render_template('index.html',
                               selections=app_config.get(),
                               dashboard_html=get_html(),
                               nhl_html=nhl.get_html(),
                               nfl_html=nfl.get_html(),
                               config_html=Markup(render_template('packages/app_config.html',
                                                                  selections=app_config.get())))


# Dashboard HTML Generation
def get_html():

    return Markup(render_template('packages/dashboard.html', selections=app_config.get()))


@bp.route('/config', defaults={"command": None}, methods=['POST'])
@bp.route('/config/<string:command>', methods=['POST'])
def config_handler(command):

    if command == "download":

        return send_file('app_config.json', attachment_filename='Hue_Score_Alert_config.json', as_attachment=True)

    elif command == "upload":

        try:

            upload = request.files['file']

            upload.save('HueScoreAlert/app_config.json')

            return redirect(url_for(".index"))

        except KeyError:

            return redirect(url_for(".index"))

    else:

        return redirect(url_for(".index"))


@bp.route('/bridge', methods=['POST'])
def set_bridge():

    bridge_ip = request.form["bridge_ip"]

    app_config.save("bridge_ip", bridge_ip)

    # FixMe - Determine Host Error and place here
    if app_config.get()["user_token"] != "PLACEHOLDER":

        user_token = hue.create_user()

        if user_token == "link button not pressed":

            return redirect(url_for(".index"))

        app_config.save("user_token", user_token)

    return redirect(url_for(".index"))

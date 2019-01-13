from flask import Blueprint, redirect, render_template, url_for

# Creates Blueprint
bp = Blueprint('hue', __name__, url_prefix='/hue')


# Initial Route Page
@bp.route('/hello')
def hello():

    return 'Hello Hue World!'

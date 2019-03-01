import HueScoreAlert
import logging
import subprocess
from waitress import serve

subprocess.Popen('celery -A HueScoreAlert.nhl worker'.split(), stdout=subprocess.PIPE)

serve(HueScoreAlert.create_app(), listen='0.0.0.0:8080')

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

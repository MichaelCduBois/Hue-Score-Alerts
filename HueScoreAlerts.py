import HueScoreAlert
import logging
from waitress import serve

serve(HueScoreAlert.create_app(), listen='0.0.0.0:8080')

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

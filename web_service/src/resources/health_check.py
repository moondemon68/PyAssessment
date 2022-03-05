from flask_restful import Resource
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response

class HealthCheck(Resource):
  def __init__(self):
    self.logger = create_logger()

  def get(self):
    self.logger.info("receiving health check request")
    return get_response(err=False, msg='Healthy')
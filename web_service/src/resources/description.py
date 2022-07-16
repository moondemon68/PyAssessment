from flask_restful import Resource
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response

class Description(Resource):
  def __init__(self):
    self.logger = create_logger()

  def get(self):
    self.logger.info("receiving description request")
    return get_response(err=False, msg='success', data={
      "imageName": "moondemon68/py-assessment",
      "displayedName": "Semantic Based White Box Autograder",
      "description": "White Box Autograder for Python Functions"
    })
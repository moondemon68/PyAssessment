from flask_restful import Resource
from flask import request
from web_service.src.utils.check_file import check_file
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response
from http import HTTPStatus
from grader.grading import semi_whitebox_grade
from werkzeug.utils import secure_filename
import uuid
import os

class SemiWhiteboxGrade(Resource):
  def __init__(self):
    self.logger = create_logger()

  def post(self):
    self.logger.info("receiving semi whitebox grade request")

    if 'src_ref' not in request.files:
      return get_response(err=True, msg='src_ref required', status_code=HTTPStatus.BAD_REQUEST)
    if 'src' not in request.files:
      return get_response(err=True, msg='src required', status_code=HTTPStatus.BAD_REQUEST)
    
    random_uuid = uuid.uuid4().hex
    if not os.path.exists(os.path.join('/tmp', random_uuid)):
      os.makedirs(os.path.join('/tmp', random_uuid))

    src_ref = request.files['src_ref']
    err_file, msg_file = check_file(src_ref)
    src_ref_filename = os.path.join('/tmp', random_uuid, secure_filename(src_ref.filename))
    if err_file:
      return get_response(err=True, msg='error reading src_ref: ' + msg_file, status_code=HTTPStatus.BAD_REQUEST)
    else:
      try:
        src_ref.save(src_ref_filename)
      except:
        return get_response(err=True, msg='error saving src_ref to ' + src_ref_filename, status_code=HTTPStatus.BAD_REQUEST)
    
    src = request.files['src']
    err_file, msg_file = check_file(src)
    src_filename = os.path.join('/tmp', random_uuid, secure_filename(src.filename))
    if err_file:
      return get_response(err=True, msg='error reading src: ' + msg_file, status_code=HTTPStatus.BAD_REQUEST)
    else:
      try:
        src.save(src_filename)
      except:
        return get_response(err=True, msg='error saving src to ' + src_filename, status_code=HTTPStatus.BAD_REQUEST)
    
    try:
      result = semi_whitebox_grade(src_ref_filename, src_filename, 25, 1)
      return result
    except Exception as e:
      self.logger.error('an error occured:', e)
      return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
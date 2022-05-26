from flask_restful import Resource
from flask import request
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response
from http import HTTPStatus
from grader.grading import random_grade
from werkzeug.utils import secure_filename
import uuid
import os
import base64
from func_timeout import func_timeout, FunctionTimedOut

class RandomGrade(Resource):
  def __init__(self):
    self.logger = create_logger()

  def post(self):
    self.logger.info("receiving whitebox grade request")

    request_data = request.get_json()

    # check request data is valid
    mandatory_attributes = ['references', 'referencesFileNames', 'solution', 'solutionFileName', 'timeLimit']
    if not request_data or not all(key in request_data for key in mandatory_attributes):
      return get_response(
        err=True,
        msg="invalid request body",
        status_code=HTTPStatus.BAD_REQUEST
      )
    if not isinstance(request_data['references'], list):
      return get_response(
        err=True,
        msg="references must be a list of string",
        status_code=HTTPStatus.BAD_REQUEST
      )
    if not isinstance(request_data['referencesFileNames'], list):
      return get_response(
        err=True,
        msg="referencesFileNames must be a list of string",
        status_code=HTTPStatus.BAD_REQUEST
      )
    if not isinstance(request_data['solution'], str):
      return get_response(
        err=True,
        msg="solution must be a string",
        status_code=HTTPStatus.BAD_REQUEST
      )
    if not isinstance(request_data['solutionFileName'], str):
      return get_response(
        err=True,
        msg="solutionFileName must be a string",
        status_code=HTTPStatus.BAD_REQUEST
      )
    if not isinstance(request_data['timeLimit'], int):
      return get_response(
        err=True,
        msg="timeLimit must be an integer",
        status_code=HTTPStatus.BAD_REQUEST
      )
    
    # generate random uuid to make unique file/function name
    random_uuid = 'a' + uuid.uuid4().hex
    
    encoded_reference_file = request_data['references'][0]
    reference_file_name = request_data['referencesFileNames'][0]
    encoded_solution_file = request_data['solution']
    solution_file_name = request_data['solutionFileName']
    time_limit = request_data['timeLimit']

    # decode base64 and save reference file
    reference_file_path = os.path.join('/tmp', random_uuid + '_' + secure_filename(reference_file_name))
    try:
      reference_file = base64.b64decode(encoded_reference_file).decode('utf-8')
    except Exception as e:
      self.logger.error(e)
      return get_response(
        err=True,
        msg="invalid reference file",
        status_code=HTTPStatus.BAD_REQUEST
      )
    with open(reference_file_path, 'w') as f:
      f.write(reference_file)

    # decode base64 and save solution file
    solution_file_path = os.path.join('/tmp', random_uuid + '_' + secure_filename(solution_file_name))
    try:
      solution_file = base64.b64decode(encoded_solution_file).decode('utf-8')
    except Exception as e:
      self.logger.error(e)
      return get_response(
        err=True,
        msg="invalid solution file",
        status_code=HTTPStatus.BAD_REQUEST
      )
    with open(solution_file_path, 'w') as f:
      f.write(solution_file)

    # replace function name
    fin = open(reference_file_path, "r")
    data = fin.read()
    data = data.replace('def ' + secure_filename(reference_file_name[:-3]), 'def ' + random_uuid + '_' + secure_filename(reference_file_name[:-3]))
    fin.close()
    fin = open(reference_file_path, "w")
    fin.write(data)
    fin.close()

    fin = open(solution_file_path, "r")
    data = fin.read()
    data = data.replace('def ' + secure_filename(solution_file_name[:-3]), 'def ' + random_uuid + '_' + secure_filename(solution_file_name[:-3]))
    fin.close()
    fin = open(solution_file_path, "w")
    fin.write(data)
    fin.close()

    try:
      result = func_timeout(time_limit / 1000, random_grade, args=(reference_file_path, solution_file_path, -100, 100))
      # cleanup
      os.remove(reference_file_path)
      os.remove(solution_file_path)

      returned_data = {
        'grade': result['grade']
      }

      return get_response(
        err=False,
        msg="success",
        data=returned_data,
      )
    except FunctionTimedOut as e:
      # cleanup
      os.remove(reference_file_path)
      os.remove(solution_file_path)

      return get_response(err=True, msg='Time limit exceeded', status_code=HTTPStatus.OK)
    except AttributeError as e:
      # cleanup
      os.remove(reference_file_path)
      os.remove(solution_file_path)

      return get_response(err=True, msg='Filename mismatch', status_code=HTTPStatus.OK)
    except NameError as e:
      # cleanup
      os.remove(reference_file_path)
      os.remove(solution_file_path)

      return get_response(err=True, msg='syntax error', status_code=HTTPStatus.OK)
    except Exception as e:
      # cleanup
      os.remove(reference_file_path)
      os.remove(solution_file_path)

      return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
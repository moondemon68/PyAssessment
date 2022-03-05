from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck
from web_service.src.resources.random_grade import RandomGrade
from web_service.src.resources.semi_whitebox_grade import SemiWhiteboxGrade
from web_service.src.resources.whitebox_grade import WhiteboxGrade

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/health-check')
api.add_resource(RandomGrade, '/random-grade')
api.add_resource(SemiWhiteboxGrade, '/semi-whitebox-grade')
api.add_resource(WhiteboxGrade, '/grade')

if __name__ == '__main__':
  app.run(host="0.0.0.0")
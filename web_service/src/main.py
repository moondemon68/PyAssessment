from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/healthcheck')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
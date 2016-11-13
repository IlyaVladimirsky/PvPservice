from flask import Flask
from flask_restful import Api, Resource

from match_logic import MatchLogic

API_ROUTE = '/api/match'

app = Flask(__name__)
api = Api(app)
logic = MatchLogic


class MatchResource(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

api.add_resource(MatchResource, API_ROUTE)

if __name__ == '__main__':
    app.run(debug=True)

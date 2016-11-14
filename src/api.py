from flask import Flask
from flask import request, jsonify
from flask_restful import Api, Resource

from match_logic import MatchLogic

API_ROUTE = '/api/match'

app = Flask(__name__)
api = Api(app)
logic = MatchLogic()


class MatchResource(Resource):
    def get(self):
        pass

    def post(self):
        data = request.json
        if 'nickname' not in data:
            return jsonify(logic.get_error_message('Incorrect POST parameters'))
        else:
            nickname = data['nickname']
            ip = request.environ['REMOTE_ADDR']

            return jsonify(logic.create_match_request(nickname, ip))

    def put(self):
        pass

    def delete(self):
        pass

api.add_resource(MatchResource, API_ROUTE)

if __name__ == '__main__':
    app.run(debug=True)

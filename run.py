from asyncio import get_event_loop, new_event_loop

from flask import Flask
from flask_restful import Api

from src.match_api import MatchResource
from src.match_logic import MatchLogic

API_ROUTE = '/api/match'
CLIENTS_NUMBER = 5
MATCH_WAIT_TIME = 2

app = Flask(__name__)
api = Api(app)
logic = MatchLogic(
    clients_number=CLIENTS_NUMBER,
    match_wait_time=MATCH_WAIT_TIME
)

api.add_resource(MatchResource, API_ROUTE, resource_class_kwargs={'logic': logic, 'loop': get_event_loop()})

if __name__ == '__main__':
    app.run(debug=True)

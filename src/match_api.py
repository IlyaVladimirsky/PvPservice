import asyncio

from flask import request, jsonify
from flask_restful import Resource


class MatchResource(Resource):
    def __init__(self, logic, loop):
        self.logic = logic
        self.loop = loop

    def get(self):
        pass

    def post(self):
        data = request.json
        if 'nickname' not in data:
            return jsonify(self.logic.get_error_response('Incorrect POST parameters'))
        else:
            client_info = {
                'nickname': data['nickname'],
                'ip':       request.environ['REMOTE_ADDR']
            }

            asyncio.set_event_loop(self.loop)
            task = asyncio.ensure_future(self.logic.create_match_request(**client_info))
            self.loop.run_until_complete(task)

            return jsonify(task.result())

    def put(self):
        pass

    def delete(self):
        pass

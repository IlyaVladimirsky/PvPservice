import asyncio
import logging
from flask import request, jsonify
from flask_restful import Resource

import src.logger as logger


class MatchResource(Resource):
    """Class docs here"""

    def __init__(self, logic, loop, debug=True):
        """Init docs here"""
        self.logic = logic
        self.loop = loop

        self.logger = logger.get_logger(
            name=__name__,
            path='logs/debug.log',
            level=logging.DEBUG,
            formatter='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self._debug = debug

    def get(self):
        pass

    def post(self):
        """Method docs here"""
        data = request.json
        if 'nickname' not in data:
            return jsonify(self.logic.get_error_response('Incorrect POST parameters'))
        else:
            client_info = {
                'nickname': data['nickname'],
                'ip':       request.environ['REMOTE_ADDR']
            }

            self.logger.debug('[post]: %s before event loop', client_info['nickname'])
            asyncio.set_event_loop(self.loop)
            task = asyncio.ensure_future(self.logic.create_match_request(**client_info))
            self.loop.run_until_complete(task)

            return jsonify(task.result())

    def put(self):
        pass

    def delete(self):
        pass

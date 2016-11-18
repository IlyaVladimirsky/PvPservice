import asyncio
import logging
from asyncio import Event, Lock

import src.logger as logger
from .singleton import Singleton


@Singleton
class MatchLogic:
    """Class docs here"""

    def __init__(self, clients_number=2, match_wait_time=1, debug=True):
        """Init docs here"""

        # TODO: db class
        self._clients_number = clients_number
        self._match_wait_time = match_wait_time

        self._event_lock = Event()
        self._count_lock = Lock()
        self._waiting_count = 0

        self._match_id = None

        self.logger = logger.get_logger(
            name=__name__,
            path='logs/debug.log',
            level=logging.DEBUG,
            formatter='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self._debug = debug

    async def create_match_request(self, **client_info):
        """Method docs here"""

        self.logger.debug('[create_match_request]: %s enter', client_info['nickname'])

        # here the info about the client may be saved in db

        with await self._count_lock:
            self._waiting_count += 1

            if self._waiting_count == self.clients_number:
                self._waiting_count = 0

                # TODO: create and store new match in db
                self._match_id = 1
                player_id = 1  # TODO: generate client id for the _match_id

                self.logger.debug('[create_match_request]: %s unlocked event locker', client_info['nickname'])
                self._event_lock.set()

                await asyncio.sleep(0.00001)  # wait while other clients will be released from waiting
                self.logger.debug('[create_match_request]: %s locked event locker', client_info['nickname'])
                self._event_lock.clear()

                self.logger.debug('[create_match_request]: %s  - return success response', client_info['nickname'])
                return self._get_match_response(self._match_id, **{
                        'player_id': player_id,
                        **client_info
                    }
                )

        self.logger.debug('[create_match_request]: waiting count = %d', self._waiting_count)
        if not self._event_lock.is_set():
            try:
                self.logger.debug('[create_match_request]: %s is waiting', client_info['nickname'])
                await asyncio.wait_for(self._event_lock.wait(), self.match_wait_time)
                player_id = 1  # TODO: generate client id for the _match_id

                self.logger.debug('[create_match_request]: %s  - return success response', client_info['nickname'])
                return self._get_match_response(self._match_id, **{
                        'player_id': player_id,
                        **client_info
                    }
                )
            except asyncio.TimeoutError:
                self.logger.debug('[create_match_request]: %s - TimeoutError', client_info['nickname'])
                await self._dec_counter()

                self.logger.debug('[create_match_request]: %s  - return fail response', client_info['nickname'])
                return self.get_error_response('timeout')

    async def _inc_counter(self):
        """Method docs here"""

        with await self._count_lock:
            self._waiting_count += 1

    async def _dec_counter(self):
        """Method docs here"""

        with await self._count_lock:
            self._waiting_count -= 1

    def _get_match_response(self, match_id, **player_info):
        return {
            'match_id': match_id,
            'player_info': player_info
        }

    @property
    def clients_number(self):
        return self._clients_number

    @clients_number.setter
    def clients_number(self, new_number):
        self._clients_number = new_number

    @property
    def match_wait_time(self):
        return self._match_wait_time

    @match_wait_time.setter
    def match_wait_time(self, new_wait_time):
        self._match_wait_time = new_wait_time

    @property
    def debug(self):
        return self._debug

    @match_wait_time.setter
    def debug(self, new_debug_mode):
        self._debug = new_debug_mode

    def get_error_response(self, text):
        """Method docs here"""

        return {'error': text}

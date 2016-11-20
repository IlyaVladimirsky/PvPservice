import asyncio
from asyncio import Event, Lock

from src.match_database import MatchDB
from .singleton import Singleton


@Singleton
class MatchLogic:
    """Class docs here"""

    def __init__(self, clients_number, match_wait_time, logger, debug=True):
        """Init docs here"""

        self._match_db = MatchDB()

        self._clients_number = clients_number
        self._match_wait_time = match_wait_time

        self._event_lock = Event()
        self._count_lock = Lock()
        self._unique_id_lock = Lock()
        self._waiting_count = 0

        self._unique_player_ids = []
        self._match_id = None

        self._log = logger
        self._debug = debug

    async def create_match_request(self, **client_info):
        """Method docs here"""

        self._log.debug('[create_match_request]: %s enter', client_info['nickname'])

        # here the info about the client may be saved in db

        with await self._count_lock:
            self._waiting_count += 1

            if self._waiting_count == self.clients_number:
                self._waiting_count = 0

                self._match_id = self._match_db.create_match()
                self._unique_player_ids = list(range(self.clients_number))

                unique_player_id = await self._get_unique_player_id()
                player_id = self._match_db.register_player(**client_info)
                self._match_db.assign_player_to_match(self._match_id, player_id, unique_player_id)

                self._log.debug('[create_match_request]: %s unlocked event locker', client_info['nickname'])
                self._event_lock.set()

                await asyncio.sleep(0.00001)  # wait while other clients will be released from waiting
                self._log.debug('[create_match_request]: %s locked event locker', client_info['nickname'])
                self._event_lock.clear()

                self._log.debug('[create_match_request]: %s  - return success response', client_info['nickname'])
                return self._get_match_response(self._match_id, **{
                        'player_id': unique_player_id,
                        **client_info
                    }
                )

        self._log.debug('[create_match_request]: waiting count = %d', self._waiting_count)
        if not self._event_lock.is_set():
            try:
                self._log.debug('[create_match_request]: %s is waiting', client_info['nickname'])
                await asyncio.wait_for(self._event_lock.wait(), self.match_wait_time)

                self._log.debug('[create_match_request]: %s  - enter in _get_unique_player_id()', client_info['nickname'])
                unique_player_id = await self._get_unique_player_id()
                player_id = self._match_db.register_player(**client_info)
                self._match_db.assign_player_to_match(self._match_id, player_id, unique_player_id)

                self._log.debug('[create_match_request]: %s  - return success response', client_info['nickname'])
                return self._get_match_response(self._match_id, **{
                        'player_id': unique_player_id,
                        **client_info
                    }
                )
            except asyncio.TimeoutError:
                self._log.debug('[create_match_request]: %s - TimeoutError', client_info['nickname'])
                await self._dec_counter()

                self._log.debug('[create_match_request]: %s  - return fail response', client_info['nickname'])
                return self.get_error_response('timeout')

    async def _inc_counter(self):
        """Method docs here"""

        with await self._count_lock:
            self._waiting_count += 1

    async def _dec_counter(self):
        """Method docs here"""

        with await self._count_lock:
            self._waiting_count -= 1

    async def _get_unique_player_id(self):
        """Method docs here"""

        with await self._unique_id_lock:
            self._log.debug('[_get_unique_player_id]: %s  - unique', self._unique_player_ids)
            return self._unique_player_ids.pop(0) if len(self._unique_player_ids) > 0 else None

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

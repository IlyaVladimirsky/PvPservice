import asyncio
from asyncio import Event, Lock

from src.match_database import MatchDB
from .singleton import Singleton


@Singleton
class MatchLogic:
    """Class allows synchronize asynchronous client requests to match creating.

    Note:
        Class always has one instance.
    """

    def __init__(self, clients_number, match_wait_time, logger):
        """Initialize important parameters to create a match.

        Args:
            clients_number: count of the players taking part in the match.
            match_wait_time: request timeout for the client.
            logger: log object.
        """

        self._match_db = MatchDB()  # allows interact with Match database

        self._clients_number = clients_number
        self._match_wait_time = match_wait_time

        self._event_lock = Event()  # used for waiting and notifying other players
        self._count_lock = Lock()  # used to synchronize access to counter sections
        self._unique_id_lock = Lock()  # used to synchronize access to unique_player_ids variable
        self._waiting_count = 0  # count of clients waiting while match will be created

        self._unique_player_ids = []  # when match has been created each players get one of this
        self._match_id = None  # match id obtained when new match record is creating in database

        self._log = logger

    async def create_match_request(self, **client_info):
        """Wait for needed count of clients and return informative response for each player.

        Every client, when arrived, get into counter critical section, where he increment counter and
        look whether now number of waiting clients is enough to create the match.
        If true, arrived client creates match in db, sets counter to zero and releases waiting clients from
        event lock, after follows a delay so the waiting have a time to be released, then the same client
        unlock event counter to make new clients wait and return success response to the client.
        Else arrived client becomes a waiting and waits for locking event counter to be released and then
        return successful response. But if client waits more than `match_wait_time`, then TimeOut exception
        is rising. In this case client get error response.

        Args:
            client_info: information about arrived client.

        Returns:
            Structured response (see docs of get_match_response method).
        """

        self._log.debug('[create_match_request]: %s enter', client_info['nickname'])

        with await self._count_lock:
            self._waiting_count += 1

            if self._waiting_count == self.clients_number:
                self._waiting_count = 0

                self._match_id = self._match_db.create_match()
                self._unique_player_ids = list(range(self.clients_number))  # updated each new match

                unique_player_id = await self._register_to_match(**client_info)

                self._log.debug('[create_match_request]: %s unlocked event locker', client_info['nickname'])
                self._event_lock.set()

                await asyncio.sleep(0.00001)  # wait while other clients will be released from waiting
                self._log.debug('[create_match_request]: %s locked event locker', client_info['nickname'])
                self._event_lock.clear()

                self._log.debug('[create_match_request]: %s  - return success response', client_info['nickname'])
                return self._get_match_response(self._match_id, unique_player_id, **client_info)

        self._log.debug('[create_match_request]: waiting count = %d', self._waiting_count)
        if not self._event_lock.is_set():
            try:
                self._log.debug('[create_match_request]: %s is waiting', client_info['nickname'])
                await asyncio.wait_for(self._event_lock.wait(), self.match_wait_time)

                unique_player_id = await self._register_to_match(**client_info)

                self._log.debug('[create_match_request]: %s  - return success response', client_info['nickname'])
                return self._get_match_response(self._match_id, unique_player_id, **client_info)
            except asyncio.TimeoutError:
                self._log.debug('[create_match_request]: %s - TimeoutError', client_info['nickname'])
                await self._dec_counter()

                self._log.debug('[create_match_request]: %s  - return fail response', client_info['nickname'])
                return self.get_error_response('timeout')

    async def _inc_counter(self):
        """Increment waiting counter using count lock."""

        with await self._count_lock:
            self._waiting_count += 1

    async def _dec_counter(self):
        """Decrement waiting counter using count lock."""

        with await self._count_lock:
            self._waiting_count -= 1

    async def _register_to_match(self, **client_info):
        """Register a client to the match.

        Find unique player id for the match and his id in db, then use it for registering
        player to the match.

        Args:
            client_info: information about the client.

        Returns:
            Unique player id for the match.
        """
        self._log.debug('[register_to_match]: %s is registered to the match', client_info['nickname'])

        unique_player_id = await self._get_unique_player_id()
        player_id = self._match_db.register_player(**client_info)
        self._match_db.assign_player_to_match(self._match_id, player_id, unique_player_id)

        return unique_player_id

    async def _get_unique_player_id(self):
        """Generate unique player id.

        Note:
            `unique_player_ids` must be initialized already.

        Returns:
            First id from `unique_player_ids`, if it contains elements and None otherwise.
        """

        with await self._unique_id_lock:
            return self._unique_player_ids.pop(0) if len(self._unique_player_ids) > 0 else None

    def _get_match_response(self, match_id, unique_player_id, **client_info):
        """Return successful match response.

        Args:
            match_id: id of created match.
            unique_player_id: unique id in the match.
            client_info: information about the client.

        Returns:
            Structured response.

        Example:
            {
                'match_id': 1,
                'player_info':
                {
                    'player_id': 3,
                    'nickname': 'Nick',
                    'ip': '0.0.0.0'
                }
            }
        """
        return {
            'match_id': match_id,
            'player_info': {
                'player_id': unique_player_id,
                **client_info
            }
        }

    def get_error_response(self, text):
        """Return error response.

        Args:
            text: text of an error.

        Returns:
            Structured response.

        Example:
            {
                'error': 'This is fail'
            }
        """

        return {'error': text}

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

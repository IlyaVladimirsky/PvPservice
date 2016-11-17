import unittest
from unittest import TestCase
from contextlib import closing
import asyncio

import src.match_logic as match_logic


async def client(logic, delay, **info):
    # await asyncio.sleep(delay)

    return await logic.create_match_request(**info)


class TestMatchLogic(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logic = match_logic.MatchLogic()

    def test_if_connected_clients_number_is_equal_limit_clients_number(self):
        clients_count = 3
        TestMatchLogic.logic.clients_number = clients_count

        with closing(asyncio.get_event_loop()) as loop:
            tasks = [asyncio.ensure_future(client(
                TestMatchLogic.logic, i, **{'nickname': chr(ord("A") + i), 'ip': i})) for i in range(clients_count)]
            loop.run_until_complete(asyncio.gather(*tasks))
            self.assertTrue(all([
                                    'player_info' in t.result() and
                                    t.result()['player_info']['nickname'] in ['A', 'B', 'C']
                                    for t in tasks
                            ]))
            # print([t.result() for t in tasks])

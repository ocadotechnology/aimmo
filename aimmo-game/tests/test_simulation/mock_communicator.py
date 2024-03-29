DUMMY_GAME_METADATA = {
    "main_avatar": 1,
    "users": [
        {
            "id": 1,
            "code": "class Avatar(object):\n"
            "    def next_turn(self, world_view, events):\n"
            "        from simulation.action import WaitAction\n"
            "        return WaitAction()\n",
        },
        {
            "id": 2,
            "code": "class Avatar(object):\n"
            "    def next_turn(self, world_view, events):\n"
            "        from simulation.action import WaitAction\n"
            "        return WaitAction()\n",
        },
    ],
}


class MockCommunicator(object):
    def __init__(self):
        self.data = DUMMY_GAME_METADATA

    async def get_game_metadata(self):
        return self.data

    def patch_game(self, data):
        return data

    def change_code(self, avatar_id, new_code):
        users = self.data["users"]
        for i in range(len(users)):
            if users[i]["id"] == avatar_id:
                users[i]["code"] = new_code

    async def close_session(self, app):
        pass

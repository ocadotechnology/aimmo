class MockCommunicator(object):
    def __init__(self):
        self.data = {
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

    def get_game_metadata(self):
        return self.data

    def mark_game_complete(self):
        return {}

    def change_code(self, avatar_id, new_code):
        users = self.data["users"]
        for i in range(len(users)):
            if users[i]["id"] == avatar_id:
                users[i]["code"] = new_code

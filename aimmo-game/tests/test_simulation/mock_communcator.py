from simulation.communicator import Communicator

class MockCommunicator(Communicator):
    def __init__(self):
        self.data = {
            "main": {
                "parameters": [],
                "main_avatar": 1,
                "users": [
                    {
                        "id": 1,
                        "code": "class Avatar:"
                    }
                ]
            }
        }

    def get_game_metadata(self):
        return self.data

    def mark_game_complete(self, data=None):
        return {}
    
    def change_code(self, id, new_code):
        users = self.data['main']['users']
        for i in range(len(users)):
            if users[i]['id'] == id:
                users[i]['code'] = new_code

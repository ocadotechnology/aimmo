class InvalidActionException(Exception):
    def __init__(self, invalid_action_object):
        message = '"{}" is not a valid action object.'.format(invalid_action_object)
        super(InvalidActionException, self).__init__(message)

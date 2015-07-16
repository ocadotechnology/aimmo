
class InfiniteMap(object):
    def can_move_to(self, target_location):
        return True


class EmptyMap(object):
    def can_move_to(self, target_location):
        return False
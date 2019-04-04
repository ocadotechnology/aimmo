class Avatar:
    def next_turn(self, world_state, avatar_state):
        self.world_state = world_state
        self.avatar_state = avatar_state

        if world_state.get_cell(avatar_state.location).generates_score:
            return WaitAction()

        possible_directions = self.get_possible_directions()
        directions_to_emphasise = [
            d
            for d in possible_directions
            if self.is_towards(d, self.get_closest_score_location())
        ]
        return MoveAction(
            random.choice(possible_directions + (directions_to_emphasise * 5))
        )

    def is_towards(self, direction, location):
        if location:
            return self.distance_between(
                self.avatar_state.location, location
            ) > self.distance_between(self.avatar_state.location + direction, location)
        else:
            return False

    def distance_between(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_closest_score_location(self):
        score_cells = list(self.world_state.score_cells())
        if score_cells:
            return min(
                score_cells,
                key=lambda cell: self.distance_between(
                    cell.location, self.avatar_state.location
                ),
            ).location
        else:
            return None

    def get_possible_directions(self):
        directions = (direction.EAST, direction.SOUTH, direction.WEST, direction.NORTH)
        return [
            d
            for d in directions
            if self.world_state.can_move_to(self.avatar_state.location + d)
        ]

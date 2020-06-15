// JS fixtures in Cypress issue: https://github.com/cypress-io/cypress/issues/1271
module.exports = {
    MOVE_SOUTH: {
        avatarCode: {
            code:
`def next_turn(world_state, avatar_state):
    return MoveAction(direction.SOUTH)
`
        },
        expectedAction: 'MOVE_SOUTH',
        expectedLog: ``
    },
    RETURN_NOT_AN_ACTION: {
        avatarCode: {
            code:
`def next_turn(world_state, avatar_state):
    return False
`
        },
        expectedAction: 'WAIT',
        expectedLog: 
`AttributeError: 'bool' object has no attribute 'serialise'
`
    },
    SYNTAX_ERROR: {
        avatarCode: {
            code:
`def next_turn(world_state, avatar_state):
    return MoveAction(direction.)
`
        },
        expectedAction: 'MOVE_NORTH',
        expectedLog: ``
    },
    INDENTATION_ERROR: {
        avatarCode: {
            code:
`def next_turn(world_state, avatar_state):
return MoveAction(direction.NORTH)
`
        },
        expectedAction: 'MOVE_NORTH',
        expectedLog: ``
    },
    ONE_PRINT: {
        avatarCode: {
            code:
`def next_turn(world_map, avatar_state):
    print('I AM A PRINT STATEMENT')
    return MoveAction(direction.NORTH)
`
        },
        expectedAction: 'MOVE_NORTH',
        expectedLog: 
`I AM A PRINT STATEMENT
`
    },
    TWO_PRINTS: {
        avatarCode: {
            code:
`def next_turn(world_map, avatar_state):
    print('I AM A PRINT STATEMENT')
    print('I AM ALSO A PRINT STATEMENT')
    return MoveAction(direction.NORTH)
`
        },
        expectedAction: 'MOVE_NORTH',
        expectedLog: 
`I AM A PRINT STATEMENT
I AM ALSO A PRINT STATEMENT
`
    },
    PRINTS_IN_DIFFERENT_FUNCTIONS: {
        avatarCode: {
            code:
`def next_turn(world_map, avatar_state):
    foo()
    print('I AM NOT A NESTED PRINT')
    return MoveAction(direction.NORTH)

def foo():
    print('I AM A NESTED PRINT')
`
        },
        expectedAction: 'MOVE_NORTH',
        expectedLog: 
`I AM A NESTED PRINT
I AM NOT A NESTED PRINT
`
    },
    RETURN_NOT_AN_ACTION_WITH_PRINT: {
        avatarCode: {
            code:
`def next_turn(world_map, avatar_state):
    print('THIS CODE IS BROKEN')
    return None`
        },
        expectedAction: 'WAIT',
        expectedLog: 
`Exception: Make sure you are returning an action
`
    },
    GLOBAL_VARIABLE: {
        avatarCode: {
            code:
`turn_count = 0
def next_turn(world_map, avatar_state):
    global turn_count
    turn_count += 1
    print(turn_count)
    return MoveAction(direction.NORTH)
`
        },
        expectedAction: 'MOVE_NORTH'
    }
}

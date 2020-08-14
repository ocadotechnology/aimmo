/// <reference types="cypress" />

import { DEFAULT_CODE } from '../../../src/redux/features/constants'
import { testAvatarCode, checkComputedTurnResult } from '../../support/avatarCodeTester'

describe('Avatar worker', () => {
  beforeEach(() => {
    cy.login()
    cy.deleteAllGames()
    cy.addTestGame()
  })

  it('returns wait action if code does not return an action', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    return False`
    }

    const expectedAction = { action_type: 'wait' }

    const expectedLog = "AttributeError: 'bool' object has no attribute 'serialise'\n"

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('returns wait action and prints syntax warning on syntax error', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    return MoveAction(direction.)`
    }

    const expectedAction = { action_type: 'wait' }

    const expectedLog = ''

    testAvatarCode(avatarCode, expectedAction, expectedLog)

    cy.window()
      .its('store')
      .invoke('getState')
      .its('consoleLog.logs')
      .then(logs => {
        const log = logs.entries().next().value[1]
        expect(log).to.deep.equal('SyntaxError: invalid syntax\n')
      })
  })

  it('returns wait action and prints indentation warning on indentation error', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
return MoveAction(direction.NORTH)`
    }

    const expectedAction = { action_type: 'wait' }

    const expectedLog = ''

    testAvatarCode(avatarCode, expectedAction, expectedLog)

    cy.window()
      .its('store')
      .invoke('getState')
      .its('consoleLog.logs')
      .then(logs => {
        const log = logs.entries().next().value[1]
        expect(log).to.deep.equal('IndentationError: expected an indented block\n')
      })
  })

  it('prints with one print', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    print('I AM A PRINT STATEMENT')
    return MoveAction(direction.NORTH)`
    }

    const expectedAction = {
      action_type: 'move',
      options: {
        direction: {
          x: 0,
          y: 1
        }
      }
    }

    const expectedLog = 'I AM A PRINT STATEMENT\n'

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('prints with multiple prints', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    print('I AM A PRINT STATEMENT')
    print('I AM ALSO A PRINT STATEMENT')
    return MoveAction(direction.NORTH)`
    }

    const expectedAction = {
      action_type: 'move',
      options: {
        direction: {
          x: 0,
          y: 1
        }
      }
    }

    const expectedLog = `I AM A PRINT STATEMENT
I AM ALSO A PRINT STATEMENT\n`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('prints with a print in a separate function', () => {
    const avatarCode = {
      code: `def next_turn(world_map, avatar_state):
    foo()
    print('I AM NOT A NESTED PRINT')
    return MoveAction(direction.NORTH)

def foo():
    print('I AM A NESTED PRINT')`
    }

    const expectedAction = {
      action_type: 'move',
      options: {
        direction: {
          x: 0,
          y: 1
        }
      }
    }

    const expectedLog = `I AM A NESTED PRINT
I AM NOT A NESTED PRINT\n`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('prints error message if code is broken', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    print('THIS CODE IS BROKEN')
    return None`
    }

    const expectedAction = { action_type: 'wait' }

    const expectedLog = 'Exception: Make sure you are returning an action\n'

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('stores, changes global variable and prints it out', () => {
    const avatarCode = {
      code: `turn_count = 0
def next_turn(world_map, avatar_state):
    global turn_count
    turn_count += 1
    print(turn_count)
    return MoveAction(direction.NORTH)`
    }

    const expectedAction = {
      action_type: 'move',
      options: {
        direction: {
          x: 0,
          y: 1
        }
      }
    }

    const firstExpectedLog = '1\n'

    testAvatarCode(avatarCode, expectedAction, firstExpectedLog)

    cy.fixture('gameState.json').then(gameState => {
      gameState.turnCount = 2
      cy.window()
        .its('store')
        .invoke('dispatch', {
          type: 'features/Game/SOCKET_GAME_STATE_RECEIVED',
          payload: gameState
        })
    })

    const secondExpectedLog = '2\n'
    checkComputedTurnResult(expectedAction, secondExpectedLog)
  })
})

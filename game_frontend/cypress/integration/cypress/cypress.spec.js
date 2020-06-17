/// <reference types="cypress" />

import { DEFAULT_CODE } from '../../../src/redux/features/constants'

describe('Cypress for aimmo', () => {
  beforeEach(() => {
    cy.login()
    cy.deleteAllGames()
    cy.addTestGame()
    loadGame()
  })

  it('returns wait action if code does not return an action', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    return False
`
    }

    const expectedAction = { action_type: 'wait' }

    const expectedLog = `AttributeError: 'bool' object has no attribute 'serialise'
`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

//   it('returns previous action and prints syntax warning on syntax error', () => {
//     const avatarCode = `def next_turn(world_state, avatar_state):
// return MoveAction(direction.)`

    // let editor = cy.get(".ace_text-input").first().focus()
    //
    // editor.clear()
    // editor.type(avatarCode)
    //
    // cy.get('#post-code-button').click()

    // testAvatarCode(avatarCode, expectedAction, expectedLog)

    // const consoleLog = cy.window().its('store').invoke('getState')
    //   .its('consoleLog.logs.0')
    //
    // consoleLog.then((logData) => {
    //   const message = logData['message']
    //
    //   expect(message).to.deep.equal('SyntaxError: invalid syntax\n')
    // })
  // })

  //   it('returns previous action and prints indentation warning on indentation error', () => {
  //     const avatarCode = {
  //       code:
  // `def next_turn(world_state, avatar_state):
  // return MoveAction(direction.NORTH)
  // `
  //     }

  //     const expectedAction = {
  //       action_type: 'move',
  //       options: {
  //         direction: {
  //           x: 0,
  //           y: 1
  //         }
  //       }
  //     }

  //     const expectedLog = ``

  //     testAvatarCode(avatarCode, expectedAction, expectedLog)

  //     cy.wait(2000)

  //     const consoleLog = cy.window().its('store').invoke('getState')
  //       .its('consoleLog.logs.0')

  //     consoleLog.then((logData) => {
  //       const message = logData['message']

  //       expect(message).to.deep.equal('IndentationError: expected an indented block\n')
  //     })
  //   })

  it('prints with one print', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    print('I AM A PRINT STATEMENT')
    return MoveAction(direction.NORTH)
`
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
`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('prints with multiple prints', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    print('I AM A PRINT STATEMENT')
    print('I AM ALSO A PRINT STATEMENT')
    return MoveAction(direction.NORTH)
`
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
I AM ALSO A PRINT STATEMENT
`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('prints with a print in a separate function', () => {
    const avatarCode = {
      code: `def next_turn(world_map, avatar_state):
    foo()
    print('I AM NOT A NESTED PRINT')
    return MoveAction(direction.NORTH)

def foo():
    print('I AM A NESTED PRINT')
`
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
I AM NOT A NESTED PRINT
`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

  it('prints error message if code if broken', () => {
    const avatarCode = {
      code: `def next_turn(world_state, avatar_state):
    print('THIS CODE IS BROKEN')
    return None
`
    }

    const expectedAction = { action_type: 'wait' }

    const expectedLog = `Exception: Make sure you are returning an action
`

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })

//   it('stores, changes global variable and prints it out', () => {
//     let variableValue;
//
//     const avatarCode = {
//       code: `turn_count = 0
// def next_turn(world_map, avatar_state):
//     global turn_count
//     turn_count += 1
//     print(turn_count)
//     return MoveAction(direction.NORTH)
// `
//     }
//
//     const expectedAction = {
//       action_type: 'move',
//       options: {
//         direction: {
//           x: 0,
//           y: 1
//         }
//       }
//     }
//
//     const expectedLog = `1
// `
//
//     testAvatarCode(avatarCode, expectedAction, expectedLog)

    // const getComputedTurnResult = win => {
    //   const state = win.store.getState()
    //   return state.action.avatarAction
    // }
    //
    // cy.window()
    //   .pipe(getComputedTurnResult)
    //   .should(computedTurnResult => {
    //     expect(computedTurnResult).to.not.be.undefined
    //
    //     const avatarLog = computedTurnResult.log
    //
    //     expect(avatarLog).to.deep.equal("2")
    //   })

    // const firstAvatarAction = cy.window().its('store').invoke('getState')
    //   .its('action.avatarAction')
    //
    // firstAvatarAction.then((avatarActionData) => {
    //   const avatarAction = avatarActionData['action']
    //   const log = avatarActionData['log']
    //   variableValue = parseInt(log.replace("\n", ""))
    //
    //   expect(avatarAction).to.deep.equal(expectedAction)
    // })
    //
    // cy.wait(2000)
    //
    // const nextAvatarAction = cy.window().its('store').invoke('getState')
    //   .its('action.avatarAction')
    //
    // nextAvatarAction.then((avatarActionData) => {
    //   const secondLog = avatarActionData['log']
    //   const nextVariableValue = secondLog.replace("\n", "")
    //
    //   expect(parseInt(nextVariableValue)).to.equal(variableValue+1)
    // })
  // })
})

function testAvatarCode (avatarCode, expectedAction, expectedLog) {
  const getComputedTurnResult = win => {
    const state = win.store.getState()
    return state.action.avatarAction
  }

  cy.window()
    .pipe(getComputedTurnResult)
    .should(computedTurnResult => {
      expect(computedTurnResult).to.not.be.undefined

      const avatarAction = computedTurnResult.action
      const avatarLog = computedTurnResult.log

      expect(avatarAction).to.deep.equal(expectedAction)
      expect(avatarLog).to.deep.equal(expectedLog)
    })
}

function loadGame (initialCode) {
  cy.server()
    .route('GET', 'https://pyodide-cdn2.iodide.io/v0.15.0/full/pyodide.asm.data')
    .as('getPyodide')
  cy.server()
    .route('GET', 'static/worker/aimmo_avatar_api-0.0.0-py3-none-any.whl')
    .as('getAvatarApi')

  cy.visitAGame(initialCode)

  cy.window()
    .its('store')
    .invoke('dispatch', { type: 'features/AvatarWorker/INITIALIZE_PYODIDE' })

  cy.wait('@getPyodide')
  cy.wait('@getAvatarApi')

  initialCode = { code: DEFAULT_CODE}

  cy.window()
    .its('store')
    .invoke('dispatch', { type: 'features/Editor/GET_CODE_SUCCESS', payload: initialCode })

  cy.fixture('gameState.json').then(gameState => {
    cy.window()
      .its('store')
      .invoke('dispatch', { type: 'features/Game/SOCKET_GAME_STATE_RECEIVED', payload: gameState })
  })
}

/// <reference types="cypress" />

import { testAvatarCode } from '../../support/avatarCodeTester'

describe('Avatar worker in a web worker', () => {
  before(() => {
    cy.login()
    cy.addTestGame()
    cy.logout()
  })

  beforeEach(() => {
    cy.login()
  })

  it('Gives a timeout message when the worker takes too long to respond', () => {
    const avatarCode = {
      code: `
  def next_turn(world_map, avatar_state):
      while True:
          pass
      return MoveAction(direction.NORTH)
  `
    }

    const expectedAction = {
      action_type: 'wait'
    }

    const expectedLog =
      "Hmm, we haven't had an action back from your avatar this turn. Is there a 🐞 in your code?"

    testAvatarCode(avatarCode, expectedAction, expectedLog)
  })
})

/// <reference types="cypress" />

import { DEFAULT_CODE } from '../../../src/redux/features/constants'

describe('Cypress for aimmo', () => {
  // it('can login, add and delete games', () => {
  //   cy.login()
  //
  //   cy.addTestGame()
  //
  //   cy.deleteAllGames()
  // })
  //
  // it('has default code on load', () => {
  //   cy.login()
  //
  //   cy.addTestGame()
  //
  //   cy.visitAGame()
  //
  //   const store = cy.window().its('store').invoke('getState')
  //   const code = store.its('editor').its('code')
  //
  //   code.should('deep.equal', {
  //     code: DEFAULT_CODE,
  //     codeOnServer: DEFAULT_CODE
  //   })
  // })

  it('changes direction', () => {
    cy.login()

    cy.updateCode(DEFAULT_CODE)

    cy.visitAGame()

    cy.wait(10000)

    let badCode = `def next_turn(world_state, avatar_state):
return False`

    let editor = cy.get(".ace_text-input").first().focus()

    editor.clear()
    editor.type(badCode)

    cy.wait(1000)

    cy.get('#post-code-button').click()

    cy.wait(5000)

    const store = cy.window().its('store').invoke('getState')
    const actionType = store.its('avatarAction').its('avatarAction')
      .its('action').its('action_type')

    actionType.should('deep.equal', "wait")
  })
})

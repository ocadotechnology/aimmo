/// <reference types="cypress" />

import { DEFAULT_CODE } from '../../../src/redux/features/constants'
import { SocketIO, Server } from 'mock-socket'

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
  // http://localhost:8000/kurono/api/games/3/connection_parameters/

  it('changes direction', () => {
    cy.login()

    cy.updateCode(DEFAULT_CODE)

    cy.visitAGame()
    
    cy.wait(5000)

    cy.fixture("avatar_code").then(code => {
      cy.window().its("store").invoke("dispatch", {type: "features/Editor/CHANGE_CODE", payload: code})
    })

    cy.window().its("store").invoke("dispatch", {type: "features/Editor/POST_CODE_SUCCESS"})
    cy.wait(5000)

    const store = cy.window().its('store').invoke('getState')
    const actionType = store.its('avatarAction').its('avatarAction')
      .its('action').its('action_type')

    actionType.should('deep.equal', "wait")
  })
})

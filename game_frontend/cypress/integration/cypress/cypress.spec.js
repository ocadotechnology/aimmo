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

  it('changes avatar direction', () => {
    changeAvatarCode("MOVE_SOUTH")

    const action = cy.window().its('store').invoke('getState').its('action')
      .its('avatarAction').its('action')

    action.should('deep.equal',
    {
      action_type: 'move',
      options: {
        direction: {
          x: 0,
          y: -1
        }
      }
    })

    checkLog("MOVE_SOUTH")
  })

  it('returns wait action if code does not return an action', () => {
    changeAvatarCode("RETURN_NOT_AN_ACTION")

    const action = cy.window().its('store').invoke('getState').its('action')
      .its('avatarAction').its('action')

    action.should('deep.equal', { action_type: 'wait' })

    checkLog("RETURN_NOT_AN_ACTION")
  })

  // it('returns wait action on syntax error', () => {
  //   changeAvatarCode("SYNTAX_ERROR")
  //
  //   const store = cy.window().its('store').invoke('getState')
  //   const action = store.its('avatarAction').its('avatarAction').its('action')
  //
  //   action.should('deep.equal', { "action_type": "wait"})
  // })
})

function changeAvatarCode(avatarCodeType) {
  cy.login()

  cy.updateCode(DEFAULT_CODE)

  cy.server().route('GET', 'static/worker/aimmo_avatar_api-0.0.0-py3-none-any.whl').as('getAvatarApi')

  cy.visitAGame()

  cy.fixture("avatar_code").then(json => {
    const code = json[avatarCodeType]["avatarCode"]
    cy.window().its("store").invoke("dispatch", {type: "features/Editor/CHANGE_CODE", payload: code})
  })

  cy.window().its("store").invoke("dispatch", {type: "features/Editor/POST_CODE_SUCCESS"})

  cy.wait('@getAvatarApi', {timeout: 20000})

  cy.wait(2000)
}

function checkLog(avatarCodeType) {
  cy.fixture("avatar_code").then(json => {
    const expectedLog = json[avatarCodeType]["expectedLog"]

    const log = cy.window().its('store').invoke('getState').its('action')
      .its('avatarAction').its('log')

    log.should('deep.equal', expectedLog)
  })
}

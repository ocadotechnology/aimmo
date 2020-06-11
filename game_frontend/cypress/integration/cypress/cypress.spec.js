/// <reference types="cypress" />

import { DEFAULT_CODE } from '../../../src/redux/features/constants'

describe('Cypress for aimmo', () => {
  it('can login, add and delete games', () => {
    cy.login()

    cy.addTestGame()

    cy.deleteAllGames()
  })

  it('has default code on load', () => {
    cy.login()

    cy.addTestGame()

    cy.visitAGame()

    const store = cy.window().its('store').invoke('getState')
    const code = store.its('editor').its('code')

    code.should('deep.equal', {
      code: "",
      codeOnServer: DEFAULT_CODE
    })
  })

  it('changes avatar direction', () => {
    testAvatarCode("MOVE_SOUTH")
  })

  it('returns wait action if code does not return an action', () => {
    testAvatarCode("RETURN_NOT_AN_ACTION")
  })

  it('returns wait action on syntax error', () => {
    testAvatarCode("SYNTAX_ERROR")
  })

  it('prints with one print', () => {
    testAvatarCode("ONE_PRINT")
  })

  it('prints with multiple prints', () => {
    testAvatarCode("TWO_PRINTS")
  })

  it('prints with a print in a separate function', () => {
    testAvatarCode("PRINTS_IN_DIFFERENT_FUNCTIONS")
  })

  it('prints even if code if broken', () => {
    testAvatarCode("RETURN_NOT_AN_ACTION_WITH_PRINT")
  })

  it('stores, changes global variable and prints it out', () => {
    testAvatarCode("GLOBAL_VARIABLE")

    cy.wait(2000)

    const avatarAction = cy.window().its('store').invoke('getState')
      .its('action.avatarAction')

    avatarAction.then((value) => {
      const secondLog = value['log']
      expect(secondLog).to.deep.equal('2\n')
    })
  })
})

function changeAvatarCode(avatarCodeType) {
  cy.login()

  cy.updateCode(DEFAULT_CODE)

  cy.server().route('GET', 'static/worker/aimmo_avatar_api-0.0.0-py3-none-any.whl').as('getAvatarApi')

  cy.visitAGame()

  cy.fixture("avatar_code").then(json => {
    const code = json[avatarCodeType]["avatarCode"]
    cy.window().its("store").invoke("dispatch", {type: "features/Editor/POST_CODE_REQUEST", payload: code})
  })

  cy.wait('@getAvatarApi', {timeout: 20000})

  cy.wait(1000)
}

function testAvatarCode(avatarCodeType) {
  changeAvatarCode(avatarCodeType)

  const avatarAction = cy.window().its('store').invoke('getState')
    .its('action.avatarAction')

  avatarAction.then((avatarActionData) => {
    const action = avatarActionData['action']
    const log = avatarActionData['log']

    checkAction(avatarCodeType, action)
    checkLog(avatarCodeType, log)
  })
}

function checkAction(avatarCodeType, action) {
  cy.fixture("avatar_code").then(codeJson => {
    const expectedAction = codeJson[avatarCodeType]["expectedAction"]

    cy.fixture("avatar_actions").then(actionsJson => {
      expect(action).to.deep.equal(actionsJson[expectedAction])
    })
  })
}

function checkLog(avatarCodeType, log) {
  cy.fixture("avatar_code").then(json => {
    const expectedLog = json[avatarCodeType]["expectedLog"]
    expect(log).to.deep.equal(expectedLog)
  })
}

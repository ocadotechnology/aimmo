/// <reference types="cypress" />

describe('Cypress for aimmo', () => {
  it('can login, add and delete games', () => {
    // login
    cy.login()

    cy.addTestGame()

    cy.deleteAllGames()
  })
})

/// <reference types="cypress" />

describe('Avatar Worker', () => {
  it('run the default code', () => {
    cy.login()

    cy.addTestGame()

    cy.deleteAllGames()
  })
})

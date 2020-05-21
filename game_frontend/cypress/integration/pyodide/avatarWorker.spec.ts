/// <reference types="cypress" />

describe('Avatar Worker', () => {
  it('loads', () => {
    cy.login()
    cy.addTestGame()
    cy.visitAGame()

    cy.deleteAllGames()
  })
})

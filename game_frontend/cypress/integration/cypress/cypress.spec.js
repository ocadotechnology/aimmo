/// <reference types="cypress" />

describe('Cypress for aimmo', () => {
  it('can login, add and delete games', () => {
    cy.login()

    cy.addTestGame()

    cy.deleteAllGames()
  })

  it('has expected state on load', () => {
    cy.login()
    cy.window().its('store').invoke('getState').should('deep.equal', {
      todos: [
        {
          completed: false,
          id: 0,
          text: 'Use Redux',
        },
      ],
      visibilityFilter: 'show_all',
    })
  })
})

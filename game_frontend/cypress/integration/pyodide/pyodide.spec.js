/// <reference types="cypress" />

describe('User code execution', () => {
  it('works with default code', () => {
    cy.visit('http://localhost:8000')

    // login
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin')
    cy.get('input[value="login"]').click()

    // create game
    cy.get('.dropdown-toggle').click()
    cy.get(':nth-child(5) > a').click()
    cy.get('#id_name')
      .type(
        Math.random()
          .toString(36)
          .substring(7)
      )
      .click()
    cy.get('.btn').click()
  })
})

/// <reference types="cypress" />

testLogoClickNavigatesToUrl = (url) => {
  cy.get('nav > header a[aria-label="Kurono dashboard"]').click()
  cy.url().should('eq', url)
}

testExitButtonClickNavigatesToUrl = (url) => {
  cy.get('nav > header').contains('Exit game').click()
  cy.url().should('eq', Cypress.config().baseUrl + 'teach/kurono/dashboard/')
}

describe('Teacher user', () => {
  before(() => {
    cy.login()
    cy.addTestGame()
  })

  beforeEach(() => {
    cy.login()
    cy.visitAGame()
  })

  it('navigates to dashboard when the logo is clicked', () => {
    testLogoClickNavigatesToUrl(Cypress.config().baseUrl + 'teach/kurono/dashboard/')
  })

  it('navigates to dashboard when the exit button is clicked', () => {
    testExitButtonClickNavigatesToUrl(Cypress.config().baseUrl + 'teach/kurono/dashboard/')
  })
})

describe('Student user', () => {
  before(() => {
    cy.login()
    cy.addTestGame()
    cy.logout()
  })

  beforeEach(() => {
    cy.studentLogin()
    cy.visitAGame()
  })

  it('navigates to dashboard when the logo is clicked', () => {
    testLogoClickNavigatesToUrl(Cypress.config().baseUrl + 'play/kurono/dashboard/')
  })

  it('navigates to dashboard when the exit button is clicked', () => {
    testExitButtonClickNavigatesToUrl(Cypress.config().baseUrl + 'play/kurono/dashboard/')
  })
})

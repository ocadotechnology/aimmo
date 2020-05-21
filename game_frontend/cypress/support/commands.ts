// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --

const username = 'admin'
const password = 'admin'

Cypress.Commands.add('login', () => {
  cy.request('/accounts/login/')
  cy.getCookie('csrftoken').then(csrfToken => {
    cy.request({
      method: 'POST',
      url: '/accounts/login/',
      failOnStatusCode: false,
      form: true,
      body: {
        username,
        password,
        csrfmiddlewaretoken: csrfToken.value
      }
    })
    cy.visit('/')
  })
})

Cypress.Commands.add('addTestGame', () => {
  cy.request('/games/new/')
  cy.getCookie('csrftoken').then(csrfToken => {
    cy.request({
      method: 'POST',
      url: '/games/new/',
      failOnStatusCode: false,
      form: true,
      body: {
        name: 'test',
        csrfmiddlewaretoken: csrfToken.value
      }
    })
  })
})

Cypress.Commands.add('deleteAllGames', () => {
  cy.request('/api/games/').then(response => {
    const games = response.body
    for (const gameId of Object.keys(games)) {
      cy.request({
        method: 'DELETE',
        url: `api/games/${gameId}/`
      })
    }
  })
})

Cypress.Commands.add('visitAGame', () => {
  cy.request('/api/games/').then(response => {
    const gameId = Object.keys(response.body)[0]
    cy.visit(`/play/${gameId}/`)
  })
})
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

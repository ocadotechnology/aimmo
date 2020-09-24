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

const username = 'alberteinstein@codeforlife.com'
const password = 'Password1'
const game_name = 'Cypress test game'
const user_id = 2
const class_id = 1

Cypress.Commands.add('login', () => {
  cy.request('/login/teacher/')
  cy.getCookie('csrftoken').then(csrfToken => {
    cy.request({
      method: 'POST',
      url: '/login/teacher/',
      failOnStatusCode: true,
      form: true,
      body: {
        username,
        password,
        csrfmiddlewaretoken: csrfToken.value,
        'g-recaptcha-response': 'something'
      }
    })
    cy.visit('/')
  })
})

Cypress.Commands.add('addTestGame', () => {
  cy.visit('/kurono/')

  cy.get('#create_new_game_button').click()
  cy.get('[name=name]').type(game_name)
  cy.get('#id_game_class').select('1')
  cy.get('#id_worksheet').select('2')
  cy.get('#create_game_button').click()

  return cy.url().then(url => url.split('/').pop())
})

Cypress.Commands.add('visitAGame', gameId => {
  cy.fixture('initialState.json').then(initialState => {
    cy.visit(`/kurono/play/${gameId}/`, {
      onBeforeLoad: win => {
        win.initialState = initialState
      }
    })
  })
})

Cypress.Commands.add('loadGameWithAvatarCode', (avatarCode, gameId) => {
  cy.server().route({
    method: 'GET',
    url: '/kurono/api/code/*',
    response: avatarCode
  })

  cy.visitAGame(gameId)

  cy.window()
    .its('store')
    .invoke('dispatch', { type: 'features/AvatarWorker/INITIALIZE_PYODIDE' })

  const isAvatarWorkerInitialized = win => {
    const state = win.store.getState()
    return state.avatarWorker.initialized
  }

  cy.window()
    .pipe(isAvatarWorkerInitialized, { timeout: 20000 })
    .should('eq', true)
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

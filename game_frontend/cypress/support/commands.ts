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
const worksheet_id = 1
const student_username = 'Leonardo'
const student_access_code = 'AB123'

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

Cypress.Commands.add('studentLogin', () => {
  cy.request('/login/student/')
  cy.getCookie('csrftoken').then(csrfToken => {
    cy.request({
      method: 'POST',
      url: '/login/student/',
      failOnStatusCode: true,
      form: true,
      body: {
        username: student_username,
        password,
        access_code: student_access_code,
        csrfmiddlewaretoken: csrfToken.value,
        'g-recaptcha-response': 'something'
      }
    })
    cy.visit('/')
  })
})

Cypress.Commands.add('logout', () => {
  cy.request('/logout/')
  cy.visit('/')
})

Cypress.Commands.add('addTestGame', () => {
  cy.request('/teach/kurono/dashboard/')
  cy.getCookie('csrftoken').then(csrfToken => {
    cy.request({
      method: 'POST',
      url: '/teach/kurono/dashboard/',
      failOnStatusCode: false,
      form: true,
      body: {
        name: game_name,
        game_class: class_id,
        worksheet: worksheet_id,
        csrfmiddlewaretoken: csrfToken.value
      }
    })
  })
})

Cypress.Commands.add('visitAGame', () => {
  cy.request('/kurono/api/games/').then(response => {
    const games = response.body
    // just get the first game it can find
    let testGameId = Object.keys(games)[0]
    cy.fixture('initialState.json').then(initialState => {
      cy.visit(`/kurono/play/${testGameId}/`, {
        onBeforeLoad: win => {
          win.initialState = initialState
        }
      })
    })
  })
})

Cypress.Commands.add('loadGameWithAvatarCode', avatarCode => {
  cy.intercept('GET', '/kurono/api/code/*', avatarCode)

  cy.visitAGame()

  cy.window()
    .its('store')
    .invoke('dispatch', { type: 'features/AvatarWorker/INITIALIZE_PYODIDE' })

  const isAvatarWorkerInitialized = win => {
    const state = win.store.getState()
    return state.avatarWorker.initialized
  }

  cy.window()
    .pipe(isAvatarWorkerInitialized, { timeout: 5000 })
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

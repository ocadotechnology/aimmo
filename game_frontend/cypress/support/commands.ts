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
  cy.request('/kurono/')
  cy.getCookie('csrftoken').then(csrfToken => {
    cy.request({
      method: 'POST',
      url: '/kurono/',
      failOnStatusCode: false,
      form: true,
      body: {
        name: game_name,
        game_class: class_id,
        worksheet: 2,
        csrfmiddlewaretoken: csrfToken.value
      }
    })
  })
})

Cypress.Commands.add('visitAGame', () => {
  cy.request('/kurono/api/games/').then(response => {
    const games = response.body
    let testGameId
    for (const [gameId, gameData] of Object.entries(games))
    {
      if (gameData['name'] == game_name) {
        testGameId = gameId
        break
      }
    }
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
  cy.server().route({
    method: 'GET',
    url: '/kurono/api/code/*',
    response: avatarCode
  })

  cy.visitAGame()

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

/// <reference types="cypress" />

declare namespace Cypress {
  interface Chainable {
    /**
     * Custom command to login with the default admin account that's created on the test server.
     * @example cy.login()
     */
    login(): Chainable<Element>

    /**
     * Custom command to add a game named 'test'.
     * Requires you to be logged in.
     * @example cy.addTestGame()
     */
    addTestGame(): Chainable<Element>

    /**
     * Visit the first game returned in the /api/games api.
     * @example cy.visitAGame()
     */
    visitAGame(): Chainable<Element>

    /**
     * Load and visit the first game and set its avatar code to the avatarCode object.
     * It waits for Pyodide and the Avatar API to load.
     * @example cy.loadGameWithAvatarCode({code: "test code"})
     */
    loadGameWithAvatarCode(avatarCode): Chainable<Element>
  }
}

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
     * Custom command to delete all games on the database.
     * Requires you to be logged in.
     * @example cy.deleteAllGames()
     */
    deleteAllGames(): Chainable<Element>

    /**
     * Visit the first game returned in the /api/games api.
     * @example cy.visitAGame()
     */
    visitAGame(): Chainable<Element>

    /**
     * Update the avatar's code in the first game returned in the /api/games api.
     * @param avatarCode: the string that the avatar's code should be updated to.
     * @example cy.updateCode("test code")
     */
    updateCode(avatarCode): Chainable<Element>
  }
}

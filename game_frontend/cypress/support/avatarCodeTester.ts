/// <reference types="cypress" />

export function testAvatarCode (avatarCode, expectedAction, expectedLog, gameId) {
  cy.loadGameWithAvatarCode(avatarCode, gameId)

  cy.fixture('gameState.json').then(gameState => {
    cy.window()
      .its('store')
      .invoke('dispatch', { type: 'features/Game/SOCKET_GAME_STATE_RECEIVED', payload: gameState })
  })

  checkComputedTurnResult(expectedAction, expectedLog)
}

export function checkComputedTurnResult (expectedAction, expectedLog) {
  const getComputedTurnResult = win => {
    const state = win.store.getState()
    return state.action.avatarAction
  }

  cy.window()
    .pipe(getComputedTurnResult)
    .should(computedTurnResult => {
      expect(computedTurnResult).to.not.be.undefined

      const avatarAction = computedTurnResult.action
      const avatarLog = computedTurnResult.log

      expect(avatarAction).to.deep.equal(expectedAction)
      expect(avatarLog).to.deep.equal(expectedLog)
    })
}

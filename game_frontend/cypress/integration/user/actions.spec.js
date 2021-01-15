const avatarCode = {
  code: `current code`,
  starterCode: `starter code`,
}

describe('User', () => {
  before(() => {
    cy.login()
    cy.addTestGame()
  })

  beforeEach(() => {
    cy.login()
  })

  it('resets their code to the default one in the Worksheet if they click on Reset Code and confirm', () => {
    cy.loadGameWithAvatarCode(avatarCode)
    cy.on('window:confirm', () => true)
    cy.get('button').contains('Reset code').click()
    cy.window()
      .then((win) => win.ace.edit('ace_editor').getValue())
      .should('eq', avatarCode.starterCode)
  })

  it('does not reset their code to the default one in the Worksheet if they click on Reset Code and not confirm', () => {
    cy.loadGameWithAvatarCode(avatarCode)
    cy.on('window:confirm', () => false)
    cy.get('button').contains('Reset code').click()
    cy.window()
      .then((win) => win.ace.edit('ace_editor').getValue())
      .should('eq', avatarCode.code)
  })
})

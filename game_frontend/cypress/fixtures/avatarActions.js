// JS fixtures in Cypress issue: https://github.com/cypress-io/cypress/issues/1271
module.exports = {
    MOVE_NORTH: {
        action_type: 'move',
        options: {
            direction: {
                x: 0,
                y: 1
            }
        }
    },
    MOVE_SOUTH: {
        action_type: 'move',
        options: {
            direction: {
                x: 0,
                y: -1
            }
        }
    },
    WAIT: {
        action_type: 'wait'
    }
}

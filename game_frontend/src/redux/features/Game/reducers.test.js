/* eslint-env jest */
import actions from './actions'
import gameReducer from './reducers'

describe('gameReducer', () => {
  it('should return the initial state', () => {
    expect(gameReducer(undefined, {})).toEqual({})
  })

  it('should handle SOCKET_GAME_STATE_RECEIVED', () => {
    const expectedState = {
      gameState: {
        id: 1
      },
      initialState: 'someValue'
    }
    const action = actions.socketGameStateReceived({ id: 1 })
    expect(gameReducer({initialState: 'someValue'}, action)).toEqual(expectedState)
  })
})

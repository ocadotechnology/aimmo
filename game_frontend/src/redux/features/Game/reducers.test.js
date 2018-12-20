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
      initialState: 'someValue',
      timeoutStatus: false
    }
    const action = actions.socketGameStateReceived({ id: 1 })
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should handle SOCKET_FEEDBACK_AVATAR_UPDATED', () => {
    const expectedState = {
      showSnackbarForAvatarUpdated: true,
      initialState: 'someValue'
    }
    const action = actions.socketFeedbackAvatarUpdated()
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should handle SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN', () => {
    const expectedState = {
      showSnackbarForAvatarUpdated: false,
      initialState: 'someValue'
    }
    const action = actions.snackbarForAvatarUpdatedShown()
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should handle GAME_DATA_LOADED', () => {
    const expectedState = {
      gameDataLoaded: true,
      initialState: 'someValue'
    }
    const action = actions.gameDataLoaded()
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })
})

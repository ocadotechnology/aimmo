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
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should handle SOCKET_FEEDBACK_AVATAR_UPDATED_SUCCESS', () => {
    const expectedState = {
      showSnackbar: true,
      initialState: 'someValue',
      snackbarMessage: 'Your Avatar has been updated with your new code!'
    }
    const action = actions.socketFeedbackAvatarUpdatedSuccess()
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should handle SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN', () => {
    const expectedState = {
      showSnackbar: false,
      initialState: 'someValue'
    }
    const action = actions.snackbarShown()
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

  it('should set the currentAvatarID correctly on CONNECTION_PARAMETERS_RECEIVED', () => {
    const expectedState = {
      initialState: 'someValue',
      connectionParameters: {
        currentAvatarID: 1
      }
    }

    const action = actions.connectionParametersReceived({ 'avatar_id': 1 })
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })
})

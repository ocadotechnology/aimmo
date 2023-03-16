/* eslint-env jest */
import actions from './actions'
import gameReducer from './reducers'

describe('gameReducer', () => {
  it('should return the initial state', () => {
    expect(gameReducer(undefined, {})).toEqual({})
  })

  it('should handle SOCKET_GAME_STATE_RECEIVED', () => {
    const expectedState = {
      gameLoaded: true,
      gameState: {
        id: 1,
      },
      initialState: 'someValue',
    }
    const action = actions.socketGameStateReceived({ id: 1 })
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should set the currentAvatarID correctly on CONNECTION_PARAMETERS_RECEIVED', () => {
    const expectedState = {
      initialState: 'someValue',
      connectionParameters: {
        currentAvatarID: 1,
      },
    }

    const action = actions.connectionParametersReceived({ avatar_id: 1 })
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should set cameraCenteredOnUserAvatar to false on MAP_PANNED', () => {
    const expectedState = {
      initialState: 'someValue',
      cameraCenteredOnUserAvatar: false,
    }

    const action = actions.mapPanned()
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should set cameraCenteredOnUserAvatar to true on CENTER_CAMERA_ON_USER_AVATAR', () => {
    const expectedState = {
      initialState: 'someValue',
      cameraCenteredOnUserAvatar: true,
    }

    const action = actions.centerCameraOnUserAvatar()
    expect(gameReducer({ initialState: 'someValue' }, action)).toEqual(expectedState)
  })

  it('should set gamePaused to opposite on TOGGLE_PAUSE_GAME', () => {
    const expectedState = {
      gamePaused: true,
    }

    const action = actions.togglePauseGame()
    expect(gameReducer({ gamePaused: false }, action)).toEqual(expectedState)
  })

  it('should set gamePaused to false on GAME_RESUME', () => {
    const expectedState = {
      gamePaused: false,
    }

    const action = actions.gameResume()
    expect(gameReducer({ gamePaused: true }, action)).toEqual(expectedState)
  })
})

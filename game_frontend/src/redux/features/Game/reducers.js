import types from './types'

const gameReducer = (state = {}, action) => {
  switch (action.type) {
    case types.SOCKET_GAME_STATE_RECEIVED:
      return {
        ...state,
        gameState: action.payload.gameState,
        gameLoaded: true,
      }
    case types.CONNECTION_PARAMETERS_RECEIVED:
      return {
        ...state,
        connectionParameters: {
          ...state.connectionParameters,
          currentAvatarID: action.payload.parameters.avatar_id,
        },
      }
    case types.MAP_PANNED:
      return {
        ...state,
        cameraCenteredOnUserAvatar: false,
      }
    case types.CENTER_CAMERA_ON_USER_AVATAR:
      return {
        ...state,
        cameraCenteredOnUserAvatar: true,
      }
    case types.TOGGLE_PAUSE_GAME:
      return {
        ...state,
        gamePaused: !state.gamePaused,
      }
    default:
      return state
  }
}

export default gameReducer

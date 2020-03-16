import types from './types'

const gameReducer = (state = {}, action) => {
  switch (action.type) {
    case types.SOCKET_GAME_STATE_RECEIVED:
      return {
        ...state,
        gameState: action.payload.gameState,
        gameLoaded: true
      }
    case types.SOCKET_FEEDBACK_AVATAR_UPDATED_SUCCESS:
      return {
        ...state,
        showSnackbar: true,
        snackbarMessage: 'Your Avatar has been updated with your new code!'
      }
    case types.SOCKET_FEEDBACK_AVATAR_UPDATED_TIMEOUT:
      return {
        ...state,
        showSnackbar: true,
        snackbarMessage: 'Sorry there has been a server error! Please try again in 30 seconds.'
      }
    case types.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN:
      return {
        ...state,
        showSnackbar: false
      }
    case types.CONNECTION_PARAMETERS_RECEIVED:
      return {
        ...state,
        connectionParameters: {
          ...state.connectionParameters,
          currentAvatarID: action.payload.parameters.avatar_id
        }
      }
    case types.MAP_PANNED:
      return {
        ...state,
        cameraCenteredOnUserAvatar: false
      }
    case types.CENTER_CAMERA_ON_USER_AVATAR:
      return {
        ...state,
        cameraCenteredOnUserAvatar: true
      }
    default:
      return state
  }
}

export default gameReducer

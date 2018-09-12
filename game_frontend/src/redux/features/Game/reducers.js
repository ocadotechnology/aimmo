import types from './types'

const gameReducer = (state = {}, action) => {
  switch (action.type) {
    case types.SOCKET_GAME_STATE_RECEIVED:
      return {
        ...state,
        gameState: action.payload.gameState
      }
    case types.SOCKET_FEEDBACK_AVATAR_UPDATED:
      return {
        ...state,
        showSnackbarForAvatarUpdated: true
      }
    case types.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN:
      return {
        ...state,
        showSnackbarForAvatarUpdated: false
      }
    default:
      return state
  }
}

export default gameReducer

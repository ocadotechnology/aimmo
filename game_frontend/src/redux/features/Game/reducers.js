import types from './types'

const gameReducer = (state = {}, action) => {
  switch (action.type) {
    case types.SET_TIMEOUT:
      return {
        ...state,
        timeoutStatus: true
      }
    case types.SOCKET_GAME_STATE_RECEIVED:
      return {
        ...state,
        gameState: action.payload.gameState,
        timeoutStatus: false
      }
    case types.SOCKET_FEEDBACK_AVATAR_UPDATED:
      return {
        ...state,
        showSnackbar: true,
        snackbarMessage: 'Your Avatar has been updated with your new code!'
      }
    case types.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN:
      return {
        ...state,
        showSnackbar: false
      }
    case types.GAME_DATA_LOADED:
      return {
        ...state,
        gameDataLoaded: true
      }
    default:
      return state
  }
}

export default gameReducer

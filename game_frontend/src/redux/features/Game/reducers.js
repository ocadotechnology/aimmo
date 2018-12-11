import types from './types'
import { editorTypes } from 'features/Editor'

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
        showSnackbarForAvatarUpdated: true,
        avatarUpdating: false
      }
    case types.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN:
      return {
        ...state,
        showSnackbarForAvatarUpdated: false
      }
    case types.GAME_DATA_LOADED:
      return {
        ...state,
        gameDataLoaded: true
      }
    case editorTypes.POST_CODE_REQUEST:
      return {
        ...state,
        avatarUpdating: true
      }
    default:
      return state
  }
}

export default gameReducer

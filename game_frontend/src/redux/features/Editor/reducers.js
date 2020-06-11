import { combineReducers } from 'redux'
import types from './types'
import { gameTypes } from 'features/Game'
import { avatarWorkerTypes } from 'features/AvatarWorker'
import { RunCodeButtonStatus } from 'components/RunCodeButton'
import { DEFAULT_CODE } from '../constants'

const codeReducer = (state = {}, action) => {
  switch (action.type) {
    case types.GET_CODE_SUCCESS:
      return {
        ...state,
        codeOnServer: action.payload.code
      }
    case types.POST_CODE_REQUEST:
      return {
        ...state,
        codeToBeSaved: action.payload.code
      }
    case types.POST_CODE_SUCCESS:
      return {
        ...state,
        codeOnServer: state.codeToBeSaved,
        codeToBeSaved: null
      }
    case types.RESET_CODE:
      return {
        ...state,
        resetCodeTo: DEFAULT_CODE
      }
    case types.CODE_RESET:
      return {
        ...state,
        resetCodeTo: null
      }
    default:
      return state
  }
}

const runCodeButtonReducer = (state = {}, action) => {
  switch (action.type) {
    case types.POST_CODE_REQUEST:
      return {
        ...state,
        status: RunCodeButtonStatus.updating
      }
    case avatarWorkerTypes.AVATAR_CODE_UPDATED:
      return {
        ...state,
        status: RunCodeButtonStatus.done
      }
    case gameTypes.SOCKET_GAME_STATE_RECEIVED:
      return {
        ...state,
        status: RunCodeButtonStatus.normal
      }
    default:
      return state
  }
}

export default combineReducers({
  code: codeReducer,
  runCodeButton: runCodeButtonReducer
})

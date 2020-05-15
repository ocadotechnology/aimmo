import { combineReducers } from 'redux'
import types from './types'
import { gameTypes } from 'features/Game'
import { RunCodeButtonStatus } from 'components/RunCodeButton'
import { DEFAULT_CODE } from '../constants'
import { updateAvatarCode } from '../../../pyodide/pyodideRunner'

const codeReducer = (state = { pythonInitialised: false }, action) => {
  switch (action.type) {
    case types.GET_CODE_SUCCESS:
      return {
        ...state,
        code: action.payload.code,
        codeOnServer: action.payload.code,
      }
    case types.CHANGE_CODE:
      return {
        ...state,
        code: action.payload.code,
      }
    case types.POST_CODE_SUCCESS:
      return {
        ...state,
        codeOnServer: updateAvatarCode(state.code),
      }
    case types.RESET_CODE:
      return {
        ...state,
        code: DEFAULT_CODE,
      }
    case 'PYTHON_INITIALISED':
      return {
        ...state,
        pythonInitialised: true,
        codeOnServer: updateAvatarCode(state.codeOnServer),
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
        status: RunCodeButtonStatus.updating,
      }
    case gameTypes.SOCKET_FEEDBACK_AVATAR_UPDATED_SUCCESS:
      return {
        ...state,
        status: RunCodeButtonStatus.done,
      }
    case gameTypes.SOCKET_FEEDBACK_AVATAR_UPDATED_TIMEOUT:
      return {
        ...state,
        status: RunCodeButtonStatus.error,
      }
    case gameTypes.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN:
      return {
        ...state,
        status: RunCodeButtonStatus.normal,
      }
    default:
      return state
  }
}

export default combineReducers({
  code: codeReducer,
  runCodeButton: runCodeButtonReducer,
})

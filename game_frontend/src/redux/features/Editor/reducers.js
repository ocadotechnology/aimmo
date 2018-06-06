import types from './types'

const editorReducer = (state = {}, action) => {
  // const emitUnityEvent = (unityFunction, parameter) => {
  //   if(unityFunction.canEmit())
  //   {
  //     unityFunction.emit(parameter)
  //   }
  // }

  switch (action.type) {
    case types.GET_CODE_SUCCESS:
    case types.CHANGE_CODE:
      return {
        ...state,
        code: action.payload.code
      }
    case types.GET_CONNECTION_PARAMS_SUCCESS:
      return {
        ...state,
        connectionParams: action.payload.connectionParams
      }
    default:
      return state
  }
}

export default editorReducer

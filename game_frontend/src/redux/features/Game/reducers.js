import types from './types'

const editorReducer = (state = {}, action) => {
  switch (action.type) {
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

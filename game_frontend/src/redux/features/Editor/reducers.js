import types from './types'

const editorReducer = (state = {}, action) => {
  switch (action.type) {
    case types.GET_CODE_SUCCESS:
      return {
        ...state,
        code: action.payload.code
      }
    default:
      return state
  }
}

export default editorReducer

import types from './types'

const editorReducer = (state = {}, action) => {
  switch (action.type) {
    case types.GET_CODE_SUCCESS:
      return {
        code: action.payload.code,
        ...state
      }
    default:
      return state
  }
}

export default { editorReducer }

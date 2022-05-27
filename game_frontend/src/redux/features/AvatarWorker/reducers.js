import types from './types'

const actionReducer = (state = { initialized: false }, action) => {
  switch (action.type) {
    case types.AVATARS_NEXT_ACTION_COMPUTED:
      return {
        ...state,
        avatarAction: action.payload
      }
    case types.PYODIDE_INITIALIZED:
      return {
        ...state,
        initialized: true
      }
    case types.BADGES_CHECKED:
      return {
        ...state,
        completedTasks: action.payload,
        modalOpen: true
      }
    default:
      return state
  }
}

export default actionReducer

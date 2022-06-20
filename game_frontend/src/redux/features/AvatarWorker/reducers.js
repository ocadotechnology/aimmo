import types from './types'

const actionReducer = (state = { initialized: false }, action) => {
  switch (action.type) {
    case types.AVATARS_NEXT_ACTION_COMPUTED:
      return {
        ...state,
        avatarAction: action.payload,
      }
    case types.PYODIDE_INITIALIZED:
      return {
        ...state,
        initialized: true,
      }
    case types.GET_BADGES_SUCCESS:
      return {
        ...state,
        completedBadges: action.payload,
        modalOpen: false,
      }
    case types.BADGES_EARNED:
      return {
        ...state,
        completedBadges: action.payload,
        modalOpen: true,
      }
    default:
      return state
  }
}

export default actionReducer

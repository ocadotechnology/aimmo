import types from './types'

const actionReducer = (state = {}, action) => {
  switch (action.type) {
    case types.AVATARS_NEXT_ACTION_COMPUTED:
      return {
        ...state,
        avatarAction: action.payload
      }
    default:
      return state
  }
}

export default actionReducer

import types from './types'

const movieReducer = (state = {}, action) => {
  switch (action.type) {
    case types.RECEIVE_MOVIES:
      return { movies: action.payload.movies }
    default:
      return state
  }
}

export default movieReducer

import types from './types'

const fetchMovies = () => (
  {
    type: types.FETCH_MOVIES
  }
)

const receiveMovies = movies => (
  {
    type: types.RECEIVE_MOVIES,
    payload: {
      movies
    }
  }
)

export default {
  fetchMovies,
  receiveMovies
}

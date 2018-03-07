import actions from './actions'
import types from './types'

const fetchMoviesEpic = (action$, store, { getJSON }) =>
  action$.ofType(types.FETCH_MOVIES)
    .mergeMap(action =>
      getJSON('https://ghibliapi.herokuapp.com/films')
        .map(response => actions.receiveMovies(response))
    )

export default fetchMoviesEpic

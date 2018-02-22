import { ajax } from 'rxjs/observable/dom/ajax'
import actions from './actions'
import types from './types'

const fetchMoviesEpic = action$ =>
  action$.ofType(types.FETCH_MOVIES)
    .mergeMap(action =>
      ajax.getJSON('https://ghibliapi.herokuapp.com/films')
        .map(response => actions.receiveMovies(response))
    )

export default fetchMoviesEpic

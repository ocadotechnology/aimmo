import actions from './actions'
import types from './types'
import { ofType } from 'redux-observable'
import { map, mergeMap } from 'rxjs/operators'
const fetchMoviesEpic = (action$, store$, { getJSON }) =>
  action$.pipe(
    ofType(types.FETCH_MOVIES),
    mergeMap(action =>
      getJSON('https://ghibliapi.herokuapp.com/films').pipe(
        map(response => actions.receiveMovies(response))
      )
    )
  )
export default fetchMoviesEpic

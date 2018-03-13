import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import movieReducer, { movieEpics } from './GhibliMovies'

const rootEpic = combineEpics(
  movieEpics
)

const rootReducer = combineReducers(
  movieReducer
)

export {
  rootEpic,
  rootReducer
}

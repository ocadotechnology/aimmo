import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import movieReducer, { movieEpics } from './GhibliMovies'
import editorReducer, { editorEpics } from './Editor'

const rootEpic = combineEpics(
  movieEpics,
  editorEpics
)

const rootReducer = combineReducers(
  movieReducer,
  editorReducer
)

export {
  rootEpic,
  rootReducer
}

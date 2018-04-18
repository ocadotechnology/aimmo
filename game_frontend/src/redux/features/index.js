import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import ghibliReducer, { movieEpics } from './GhibliMovies'
import editorReducer, { editorEpics } from './Editor'

const rootEpic = combineEpics(
  movieEpics,
  editorEpics
)

const rootReducer = combineReducers({
  ghibli: ghibliReducer,
  editor: editorReducer,
  game: (state = { id: 1 }) => state
})

export {
  rootEpic,
  rootReducer
}

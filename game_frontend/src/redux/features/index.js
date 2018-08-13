import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import ghibliReducer, { movieEpics } from './GhibliMovies'
import editorReducer, { editorEpics } from './Editor'
import consoleLogReducer from './ConsoleLog'
import gameReducer, { gameEpics } from './Game'

const rootEpic = combineEpics(
  movieEpics,
  ...Object.values(editorEpics),
  ...Object.values(gameEpics)
)

const rootReducer = combineReducers({
  ghibli: ghibliReducer,
  editor: editorReducer,
  game: gameReducer,
  consoleLog: consoleLogReducer
})

export {
  rootEpic,
  rootReducer
}

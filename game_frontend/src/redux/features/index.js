import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import analyticsReducer, { analyticEpics } from './Analytics'
import editorReducer, { editorEpics } from './Editor'
import consoleLogReducer from './ConsoleLog'
import gameReducer, { gameEpics } from './Game'

const rootEpic = combineEpics(
  ...Object.values(editorEpics),
  ...Object.values(gameEpics),
  ...Object.values(analyticEpics)
)

const rootReducer = combineReducers({
  editor: editorReducer,
  game: gameReducer,
  consoleLog: consoleLogReducer,
  analytics: analyticsReducer
})

export {
  rootEpic,
  rootReducer
}

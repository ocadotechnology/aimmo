import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import analyticsReducer, { analyticEpics } from './Analytics'
import actionReducer from './AvatarWorker/reducers'
import editorReducer, { editorEpics } from './Editor'
import consoleLogReducer from './ConsoleLog'
import gameReducer, { gameEpics } from './Game'
import { avatarWorkerEpics } from './AvatarWorker'

const rootEpic = combineEpics(
  ...Object.values(editorEpics),
  ...Object.values(gameEpics),
  ...Object.values(analyticEpics),
  ...Object.values(avatarWorkerEpics)
)

const rootReducer = combineReducers({
  editor: editorReducer,
  game: gameReducer,
  consoleLog: consoleLogReducer,
  analytics: analyticsReducer,
  action: actionReducer
})

export { rootEpic, rootReducer }

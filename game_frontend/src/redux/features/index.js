import { combineReducers } from 'redux'
import { combineEpics } from 'redux-observable'
import actionReducer from './AvatarWorker/reducers'
import { analyticEpics } from './Analytics'
import editorReducer, { editorEpics } from './Editor'
import consoleLogReducer from './ConsoleLog'
import gameReducer, { gameEpics } from './Game'
import avatarWorkerReducer, { avatarWorkerEpics } from './AvatarWorker'

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
  action: actionReducer,
  avatarWorker: avatarWorkerReducer
})

export { rootEpic, rootReducer }

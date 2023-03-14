import types from './types'
import { avatarWorkerTypes } from 'redux/features/AvatarWorker'
import { gameTypes } from 'redux/features/Game'
import produce from 'immer'

export const MAX_NUMBER_OF_STORED_LOGS = 600

function createNewLogMessage(workerLog, gameLog) {
  if (gameLog && workerLog) {
    return [workerLog, gameLog].join('\n')
  }
  if (gameLog) {
    return gameLog
  }
  if (workerLog) {
    return workerLog
  }
}

const consoleLogReducer = (state = { logs: new Map(), gameLog: '' }, action) => {
  switch (action.type) {
    case gameTypes.SOCKET_GAME_STATE_RECEIVED: {
      return {
        ...state,
        gameLog: action.payload.gameState.playerLog,
      }
    }
    case avatarWorkerTypes.AVATAR_CODE_UPDATED:
    case avatarWorkerTypes.AVATARS_NEXT_ACTION_COMPUTED: {
      const gameLog = state.gameLog
      const turnCount = action.payload.turnCount
      const newLogMessage = createNewLogMessage(action.payload.log, gameLog)
      if (!newLogMessage) {
        return state
      }
      const nextState = produce(state, (draftState) => {
        const logs = draftState.logs
        logs.set(turnCount, newLogMessage)
        if (logs.size > MAX_NUMBER_OF_STORED_LOGS) {
          logs.delete(logs.keys().next().value)
        }
      })
      return nextState
    }
    case types.CLEAR_CONSOLE_LOGS:
      return {
        ...state,
        logs: new Map(),
      }
    case types.APPEND_PAUSE_MESSAGE: {
      console.log('APPEND_PAUSE_MESSAGE', action.payload.turnCount);
      return {
        ...state,
      }
    }
    default:
      return state
  }
}

export default consoleLogReducer

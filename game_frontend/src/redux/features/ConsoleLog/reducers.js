import types from './types'
import { avatarWorkerTypes } from 'redux/features/AvatarWorker'
import { gameTypes } from 'redux/features/Game'

export const MAX_NUMBER_OF_STORED_LOGS = 600

function createNewLogMessage (workerLog, gameLog) {
  if (gameLog && workerLog) {
    return [gameLog, workerLog].join('\n')
  }
  if (gameLog) {
    return gameLog
  }
  if (workerLog) {
    return workerLog
  }
}

const consoleLogReducer = (state = { logs: [], workerLogs: {} }, action) => {
  switch (action.type) {
    case gameTypes.SOCKET_GAME_STATE_RECEIVED: {
      const turnCount = action.payload.gameState.turnCount
      const workerLogs = state.workerLogs
      const newLogMessage = createNewLogMessage(
        state.workerLogs[turnCount],
        action.payload.gameState.playerLog
      )
      console.log(newLogMessage)
      if (!newLogMessage) {
        return state
      }
      const newLog = {
        turnCount: turnCount,
        message: newLogMessage
      }
      let logs = [...state.logs, newLog]
      logs = logs.slice(-MAX_NUMBER_OF_STORED_LOGS)
      delete workerLogs[turnCount]
      return {
        ...state,
        workerLogs,
        logs: logs
      }
    }
    case avatarWorkerTypes.AVATAR_CODE_UPDATED:
    case avatarWorkerTypes.AVATARS_NEXT_ACTION_COMPUTED: {
      const workerLogs = state.workerLogs
      const turnCount = action.payload.turnCount
      if (workerLogs[turnCount]) {
        workerLogs[action.payload.turnCount] += `\n${action.payload.log}`
      } else {
        workerLogs[action.payload.turnCount] = action.payload.log
      }
      return {
        ...state,
        workerLogs
      }
    }
    case types.CLEAR_CONSOLE_LOGS:
      return {
        ...state,
        logs: []
      }
    default:
      return state
  }
}

export default consoleLogReducer

import types from './types'
import { avatarWorkerTypes } from 'redux/features/AvatarWorker'

export const MAX_NUMBER_OF_STORED_LOGS = 600

const consoleLogReducer = (state = { logs: [], workerLogs: {} }, action) => {
  switch (action.type) {
    case types.SOCKET_CONSOLE_LOG_RECEIVED: {
      const logsFromGame = action.payload.log
      const workerLog = state.workerLogs[logsFromGame.turn_count] ?? ''
      if (workerLog) {
        logsFromGame.message = `${workerLog}\n${logsFromGame.message}`
      }
      let logs = [...state.logs, logsFromGame]
      logs = logs.slice(-MAX_NUMBER_OF_STORED_LOGS)

      return {
        ...state,
        logs: logs
      }
    }
    case avatarWorkerTypes.AVATAR_CODE_UPDATED:
    case avatarWorkerTypes.AVATARS_NEXT_ACTION_COMPUTED: {
      const workerLogs = state.workerLogs
      workerLogs[action.payload.turnCount] = action.payload.log
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

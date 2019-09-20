import types from './types'

export const MAX_NUMBER_OF_STORED_LOGS = 600

const consoleLogReducer = (state = { logs: [] }, action) => {
  switch (action.type) {
    case types.SOCKET_CONSOLE_LOG_RECEIVED:
      let logs = [...state.logs, action.payload.log]
      logs = logs.slice(-MAX_NUMBER_OF_STORED_LOGS)

      return {
        ...state,
        logs: logs
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

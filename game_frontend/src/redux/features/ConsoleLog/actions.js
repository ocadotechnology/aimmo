import types from './types'

const socketConsoleLogReceived = (log) => ({
  type: types.SOCKET_CONSOLE_LOG_RECEIVED,
  payload: {
    log,
  },
})

const clearConsoleLogs = () => ({
  type: types.CLEAR_CONSOLE_LOGS,
})

const appendPauseMessage = (turnCount) => ({
  type: types.APPEND_PAUSE_MESSAGE,
  payload: {
    turnCount,
  },
})

export default {
  socketConsoleLogReceived,
  clearConsoleLogs,
  appendPauseMessage,
}

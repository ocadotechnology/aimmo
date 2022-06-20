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

export default {
  socketConsoleLogReceived,
  clearConsoleLogs,
}

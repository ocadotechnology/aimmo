import types from './types'

const socketConsoleLogReceived = log => ({
  type: types.SOCKET_CONSOLE_LOG_RECEIVED,
  payload: {
    log
  }
})

const clearConsoleLog = () => ({
  type: types.CLEAR_CONSOLE_LOG
})

export default {
  socketConsoleLogReceived,
  clearConsoleLog
}

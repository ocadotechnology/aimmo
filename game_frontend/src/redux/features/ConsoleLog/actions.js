import types from './types'

const socketConsoleLogReceived = log => ({
    type: types.SOCKET_CONSOLE_LOG_RECEIVED,
    payload: {
        log
    }
})

export default {
    socketConsoleLogReceived
}
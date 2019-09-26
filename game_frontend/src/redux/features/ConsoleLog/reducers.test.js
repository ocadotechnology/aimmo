/* eslint-env jest */
import consoleLogReducer, { MAX_NUMBER_OF_STORED_LOGS } from './reducers'
import actions from './actions'

describe('consoleLogReducer', () => {
  it('should return the initial state', () => {
    expect(consoleLogReducer(undefined, {})).toEqual({ logs: [] })
  })

  it('should handle SOCKET_LOG_RECEIVED', () => {
    const expectedStateLog = { turn_count: 1, message: 'Hello, good morning, I got here in my code' }

    const action = actions.socketConsoleLogReceived(expectedStateLog)
    const actualState = consoleLogReducer(undefined, action)

    expect(actualState.logs).toHaveLength(1)
    expect(actualState.logs[0].message).toEqual(expectedStateLog.message)
  })

  it('should get rid of old logs past MAX_NUMBER_OF_STORED_LOGS', () => {
    let initialLogs = Array(MAX_NUMBER_OF_STORED_LOGS - 1).fill({ turn_count: 1, message: 'Same old logs' })
    const newLog = { turn_count: 1, message: 'I\'m a new log!' }
    const ancientLogMessage = 'I\'m a new log!'
    initialLogs.unshift({ turn_count: 0, message: ancientLogMessage })

    const initialState = { logs: initialLogs }
    const action = actions.socketConsoleLogReceived(newLog)
    const actualState = consoleLogReducer(initialState, action)

    expect(actualState.logs).toHaveLength(MAX_NUMBER_OF_STORED_LOGS)
    expect(actualState.logs[MAX_NUMBER_OF_STORED_LOGS - 1].message).toEqual(newLog.message)
  })
})

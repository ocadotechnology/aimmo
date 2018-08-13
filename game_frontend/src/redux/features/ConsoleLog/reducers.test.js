/* eslint-env jest */
import consoleLogReducer, { MAX_NUMBER_OF_STORED_LOGS } from './reducers'
import actions from './actions'

describe('consoleLogReducer', () => {
  it('should return the initial state', () => {
    expect(consoleLogReducer(undefined, {})).toEqual({logs: []})
  })

  it('should handle SOCKET_LOG_RECEIVED', () => {
    const expectedStateLog = 'Hello, good morning, I got here in my code'
    
    const action = actions.socketConsoleLogReceived(expectedStateLog)
    const actualState = consoleLogReducer(undefined, action)

    expect(actualState.logs).toHaveLength(1)
    expect(actualState.logs[0].log).toEqual(expectedStateLog)
  })

  it('should get rid of old logs past MAX_NUMBER_OF_STORED_LOGS', () => {
    let initialLogs = Array(MAX_NUMBER_OF_STORED_LOGS - 1).fill({ timestamp: '1', log: 'Same old logs' })
    const newLogMessage = 'I\'m a new log!'
    const ancientLogMessage = 'I\'m a new log!'
    initialLogs.unshift({ timestamp: '0', log: ancientLogMessage })
    
    const initialState = { logs: initialLogs }
    const action = actions.socketConsoleLogReceived(newLogMessage)
    const actualState = consoleLogReducer(initialState, action)

    expect(actualState.logs).toHaveLength(MAX_NUMBER_OF_STORED_LOGS)
    expect(actualState.logs[MAX_NUMBER_OF_STORED_LOGS - 1].log).toEqual(newLogMessage)
  })
})

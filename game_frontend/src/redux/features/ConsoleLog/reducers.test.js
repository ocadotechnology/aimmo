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
    expect(consoleLogReducer(undefined, action).logs).toHaveLength(1)
    expect(consoleLogReducer(undefined, action).logs[0].log).toEqual(expectedStateLog)
  })

  it('should get rid of old logs past MAX_NUMBER_OF_STORED_LOGS', () => {
    let initialLogs = []
    
    const initialState = { logs}
  })
})

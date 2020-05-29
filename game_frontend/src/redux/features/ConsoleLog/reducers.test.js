/* eslint-env jest */
import consoleLogReducer, { MAX_NUMBER_OF_STORED_LOGS } from './reducers'
import actions from './actions'
import { avatarWorkerActions, avatarWorkerTypes } from 'redux/features/AvatarWorker'

describe('consoleLogReducer', () => {
  it('should return the initial state', () => {
    expect(consoleLogReducer(undefined, {})).toEqual({ logs: [], workerLogs: {} })
  })

  it('should handle SOCKET_LOG_RECEIVED', () => {
    const expectedStateLog = {
      turnCount: 1,
      message: 'Hello, good morning, I got here in my code'
    }

    const action = actions.socketConsoleLogReceived(expectedStateLog)
    const actualState = consoleLogReducer(undefined, action)

    expect(actualState.logs).toHaveLength(1)
    expect(actualState.logs[0].message).toEqual(expectedStateLog.message)
  })

  it('should combine workerLogs with gameLogs', () => {
    const expectedStateLog = {
      turnCount: 1,
      message: `
Hello,
I got here in my code
Game says: that's cool
`.trim()
    }
    const codeUpdatedAction = avatarWorkerActions.avatarCodeUpdated({ log: 'Hello,', turnCount: 1 })
    const nextActionComputedAction = avatarWorkerActions.avatarsNextActionComputed({
      log: 'I got here in my code',
      turnCount: 1
    })
    const gameLogAction = actions.socketConsoleLogReceived({
      turnCount: 1,
      message: "Game says: that's cool"
    })

    let state = { logs: [], workerLogs: {} }
    state = consoleLogReducer(state, codeUpdatedAction)
    state = consoleLogReducer(state, nextActionComputedAction)
    state = consoleLogReducer(state, gameLogAction)
    expect(state.logs[0]).toStrictEqual(expectedStateLog)
  })

  it('should handle CLEAR_CONSOLE_LOG', () => {
    const initialStateLog = { turnCount: 1, message: 'Hello, good morning, I got here in my code' }

    const action = actions.socketConsoleLogReceived(initialStateLog)
    const initialState = consoleLogReducer(undefined, action)

    expect(initialState.logs).toHaveLength(1)

    const clearAction = actions.clearConsoleLogs()
    const actualState = consoleLogReducer(initialState, clearAction)

    expect(actualState.logs).toHaveLength(0)
  })

  it('should get rid of old logs past MAX_NUMBER_OF_STORED_LOGS', () => {
    const initialLogs = Array(MAX_NUMBER_OF_STORED_LOGS - 1).fill({
      turnCount: 1,
      message: 'Same old logs'
    })
    const newLog = { turnCount: 1, message: "I'm a new log!" }
    const ancientLogMessage = "I'm a new log!"
    initialLogs.unshift({ turnCount: 0, message: ancientLogMessage })

    const initialState = { logs: initialLogs, workerLogs: {} }
    const action = actions.socketConsoleLogReceived(newLog)
    const actualState = consoleLogReducer(initialState, action)

    expect(actualState.logs).toHaveLength(MAX_NUMBER_OF_STORED_LOGS)
    expect(actualState.logs[MAX_NUMBER_OF_STORED_LOGS - 1].message).toEqual(newLog.message)
  })
})

/* eslint-env jest */
import consoleLogReducer, { MAX_NUMBER_OF_STORED_LOGS } from './reducers'
import { actions as gameActions } from 'features/Game'
import { avatarWorkerActions } from 'redux/features/AvatarWorker'
import actions from './actions'

describe('consoleLogReducer', () => {
  it('should return the initial state', () => {
    expect(consoleLogReducer(undefined, {})).toEqual({ logs: [], workerLogs: {} })
  })

  it('should handle GAME_STATE_RECEIVED', () => {
    const expectedStateLog = {
      turnCount: 1,
      playerLog: 'Hello, good morning, I got here in my code'
    }

    const action = gameActions.socketGameStateReceived(expectedStateLog)
    const actualState = consoleLogReducer(undefined, action)

    expect(actualState.logs).toHaveLength(1)
    expect(actualState.logs[0].message).toEqual(expectedStateLog.playerLog)
  })

  it('should combine workerLogs with gameLogs', () => {
    const expectedStateLog = {
      turnCount: 1,
      message: `
I got here in my code
Game says: that's cool
`.trim()
    }
    const nextActionComputedAction = avatarWorkerActions.avatarsNextActionComputed({
      log: 'I got here in my code',
      turnCount: 1
    })
    const gameLogAction = gameActions.socketGameStateReceived({
      turnCount: 1,
      playerLog: "Game says: that's cool"
    })

    let state = { logs: [], workerLogs: {} }
    state = consoleLogReducer(state, nextActionComputedAction)
    state = consoleLogReducer(state, gameLogAction)
    expect(state.logs[0]).toStrictEqual(expectedStateLog)
  })

  it('should handle CLEAR_CONSOLE_LOG', () => {
    const initialStateLog = {
      turnCount: 1,
      playerLog: 'Hello, good morning, I got here in my code'
    }

    const action = gameActions.socketGameStateReceived(initialStateLog)
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
    const newLog = { turnCount: 1, playerLog: "I'm a new log!" }
    const ancientLogMessage = "I'm a new log!"
    initialLogs.unshift({ turnCount: 0, message: ancientLogMessage })

    const initialState = { logs: initialLogs, workerLogs: {} }
    const action = gameActions.socketGameStateReceived(newLog)
    const actualState = consoleLogReducer(initialState, action)

    expect(actualState.logs).toHaveLength(MAX_NUMBER_OF_STORED_LOGS)
    expect(actualState.logs[MAX_NUMBER_OF_STORED_LOGS - 1].message).toEqual(newLog.playerLog)
  })
})

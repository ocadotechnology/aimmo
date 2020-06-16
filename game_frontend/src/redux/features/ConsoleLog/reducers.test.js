/* eslint-env jest */
import consoleLogReducer, { MAX_NUMBER_OF_STORED_LOGS } from './reducers'
import { actions as gameActions } from 'features/Game'
import { avatarWorkerActions } from 'redux/features/AvatarWorker'
import actions from './actions'

describe('consoleLogReducer', () => {
  it('should return the initial state', () => {
    expect(consoleLogReducer(undefined, {})).toEqual({ logs: new Map(), gameLog: '' })
  })

  it('should handle GAME_STATE_RECEIVED', () => {
    const expectedStateLog = {
      turnCount: 1,
      playerLog: 'Hello, good morning, I got here in my code'
    }

    const action = gameActions.socketGameStateReceived(expectedStateLog)
    const actualState = consoleLogReducer(undefined, action)

    expect(actualState.gameLog).toEqual(expectedStateLog.playerLog)
  })

  it('should combine workerLogs with gameLogs', () => {
    const expectedStateLog = `
I got here in my code
Game says: that's cool
`.trim()
    const gameLogAction = gameActions.socketGameStateReceived({
      turnCount: 1,
      playerLog: "Game says: that's cool"
    })
    const nextActionComputedAction = avatarWorkerActions.avatarsNextActionComputed({
      log: 'I got here in my code',
      turnCount: 1
    })

    let state = { logs: new Map(), workerLogs: {} }
    state = consoleLogReducer(state, gameLogAction)
    state = consoleLogReducer(state, nextActionComputedAction)
    expect(state.logs.get(1)).toStrictEqual(expectedStateLog)
  })

  it('should handle CLEAR_CONSOLE_LOG', () => {
    const initialLog = {
      turnCount: 1,
      log: 'Hello, good morning, I got here in my code'
    }

    const action = avatarWorkerActions.avatarsNextActionComputed(initialLog)
    const initialState = consoleLogReducer(undefined, action)

    expect(initialState.logs.size).toStrictEqual(1)

    const clearAction = actions.clearConsoleLogs()
    const actualState = consoleLogReducer(initialState, clearAction)

    expect(actualState.logs.size).toStrictEqual(0)
  })

  it('should get rid of old logs past MAX_NUMBER_OF_STORED_LOGS', () => {
    const initialLogs = new Map()
    for (let turnCount = 1; turnCount <= MAX_NUMBER_OF_STORED_LOGS; turnCount++) {
      initialLogs.set(turnCount, 'Same old logs')
    }
    const turnCountOfNewLog = MAX_NUMBER_OF_STORED_LOGS + 1
    const newLog = { turnCount: turnCountOfNewLog, log: "I'm a new log!" }
    initialLogs.set(1, "I'm the oldest log!")

    const initialState = { logs: initialLogs, workerLogs: {} }
    const action = avatarWorkerActions.avatarsNextActionComputed(newLog)
    const actualState = consoleLogReducer(initialState, action)

    expect(actualState.logs.size).toStrictEqual(MAX_NUMBER_OF_STORED_LOGS)
    expect(actualState.logs.get(turnCountOfNewLog)).toEqual(newLog.log)
  })
})

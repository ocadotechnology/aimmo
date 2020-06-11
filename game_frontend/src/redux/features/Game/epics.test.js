/* eslint-env jest */
import { pipe, of, Subject } from 'rxjs'
import { TestScheduler } from 'rxjs/testing'
import { ActionsObservable, StateObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import { actions as editorActions } from 'features/Editor'
import { delay, mapTo } from 'rxjs/operators'
import { actions as analyticActions } from 'redux/features/Analytics'
import { avatarWorkerActions } from 'features/AvatarWorker'

const deepEquals = (actual, expected) => expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('connectToGameEpic', () => {
  it('connects to the kurono game', () => {
    const gameState = {
      players: {
        id: 1,
        location: {
          x: 10,
          y: 10
        }
      }
    }

    const parameters = {
      avatar_id: 1
    }

    const marbles1 = '-a---'
    const marbles2 = '--b--'
    const values = {
      a: actions.connectionParametersReceived(parameters),
      b: actions.socketGameStateReceived(gameState)
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(testScheduler.createColdObservable(marbles1, values))

    const mockConnectToGame = () => mapTo({ type: 'socket' })

    const mockStartListeners = () =>
      pipe(delay(10, testScheduler), mapTo(actions.socketGameStateReceived(gameState)))

    const mockAPI = {
      api: {
        socket: {
          connectToGame: mockConnectToGame,
          startListeners: mockStartListeners
        }
      }
    }

    const state$ = new StateObservable(new Subject(), {})
    const actual = epics.connectToGameEpic(source$, state$, mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('getConnectionParametersEpic', () => {
  it('gets all the connection parameters', () => {
    const parameters = {
      avatar_id: 1
    }

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.socketConnectToGameRequest(),
      b: actions.connectionParametersReceived(parameters)
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(testScheduler.createColdObservable(marbles1, values))

    const mockGetJSON = () => of({ avatar_id: 1 })

    const mockAPI = {
      api: {
        get: mockGetJSON
      }
    }
    const initialState = {
      game: {
        connectionParameters: {
          game_id: 1
        }
      }
    }
    const state$ = new StateObservable(new Subject(), initialState)
    const actual = epics.getConnectionParametersEpic(source$, state$, mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('gameLoadedEpic', () => {
  it('dispatches an GAME_LOADED action only when the first game state is received', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a--b--b', {
        a: actions.socketConnectToGameRequest(),
        b: actions.socketGameStateReceived({})
      })

      const output$ = epics.gameLoadedEpic(action$)

      expectObservable(output$).toBe('-----c---', {
        c: actions.gameLoaded()
      })
    })
  })
})

describe('gameLoadedIntervalEpic', () => {
  it('measures the time taken for the game to load and sends a corresponding analytic event', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('-------a-', {
        a: actions.gameLoaded()
      })

      const state$ = null
      const output$ = epics.gameLoadedIntervalEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('-------b-', {
        b: analyticActions.sendAnalyticsTimingEvent('Kurono', 'Load', 'Game', 7)
      })
    })
  })
})

describe('codeUpdatingIntervalEpic', () => {
  it('measures the time taken for users code to update successfully and sends a corresponding analytic event', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a-b--a--b-', {
        a: editorActions.postCodeRequest(),
        b: avatarWorkerActions.avatarCodeUpdated()
      })

      const state$ = null
      const output$ = epics.codeUpdatingIntervalEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('----c-----d-', {
        c: analyticActions.sendAnalyticsTimingEvent('Kurono', 'Update', 'User code', 2, true),
        d: analyticActions.sendAnalyticsTimingEvent('Kurono', 'Update', 'User code', 3, true)
      })
    })
  })
})

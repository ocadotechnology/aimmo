/* eslint-env jest */
import { pipe, of, Subject } from 'rxjs'
import { TestScheduler } from 'rxjs/testing'
import { ActionsObservable, StateObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import { actions as editorActions } from 'features/Editor'
import api from 'api'
import { delay, mapTo } from 'rxjs/operators'
import { actions as analyticActions } from 'redux/features/Analytics'

const deepEquals = (actual, expected) =>
  expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('ReceiveGameUpdate', () => {
  it('sends game update', () => {
    const gameState = {
      'pickups': [
        {
          'type': 'invulnerability',
          'location': {
            'y': -6,
            'x': -6
          }
        }
      ],
      'obstacles': [
        {
          'orientation': 'north',
          'width': 1,
          'type': 'wall',
          'location': {
            'y': 9,
            'x': -7
          },
          'height': 1
        },
        {
          'orientation': 'north',
          'width': 1,
          'type': 'wall',
          'location': {
            'y': 4,
            'x': 9
          },
          'height': 1
        }
      ],
      'scoreLocations': [
        {
          'location': {
            'y': 10,
            'x': -15
          }
        }
      ],
      'players': [
        {
          'orientation': 'north',
          'score': 0,
          'health': 5,
          'id': 1,
          'location': {
            'y': -1,
            'x': 14
          }
        }
      ],
      'northEastCorner': {
        'y': 15,
        'x': 15
      },
      'era': 'less_flat',
      'southWestCorner': {
        'y': -15,
        'x': -15
      }
    }

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.socketGameStateReceived(gameState),
      b: actions.sendGameStateSuccess()
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockEmitToUnity = () => {
      return of(values.b)
    }

    const mockAPI = {
      api: {
        unity: {
          ...api.unity,
          emitToUnity: mockEmitToUnity
        }
      }
    }

    const state$ = new StateObservable(new Subject(), {})
    const actual = epics.sendGameStateEpic(source$, state$, mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('sendAvatarIDEpic', () => {
  it('sends avatar id', () => {
    const parameters = {
      avatar_id: 1
    }
    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.connectionParametersReceived(parameters),
      b: actions.unitySendAvatarIDSuccess()
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockEmitToUnity = () => {
      return of(values.b)
    }

    const mockAPI = {
      api: {
        unity: {
          ...api.unity,
          emitToUnity: mockEmitToUnity

        }
      }
    }

    const state$ = new StateObservable(new Subject(), {})
    const actual = epics.sendAvatarIDEpic(source$, state$, mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('connectToGameEpic', () => {
  it('connects to the aimmo game', () => {
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
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockConnectToGame = () =>
      mapTo({ type: 'socket' })

    const mockStartListeners = () =>
      pipe(
        delay(10, testScheduler),
        mapTo(actions.socketGameStateReceived(gameState))
      )

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
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockGetJSON = () =>
      of({ avatar_id: 1 })

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
        c: actions.gameDataLoaded()
      })
    })
  })
})

describe('avatarUpdatingTimeoutEpic', () => {
  it('dispatches an SET_TIMEOUT action when we sent code to update the avatar but nothing has come back in 25s', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a--a-- 24999ms -', {
        a: editorActions.postCodeRequest()
      })

      const state$ = null
      const output$ = epics.avatarUpdatingTimeoutEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('------ 24999ms b--', {
        b: actions.socketFeedbackAvatarUpdatedTimeout()
      })
    })
  })

  it('does not dispatch an SET_TIMEOUT action when we sent code to update the avatar and it does not timeout', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a--- 10s -b--a--b--', {
        a: editorActions.postCodeRequest(),
        b: actions.socketFeedbackAvatarUpdatedSuccess()
      })

      const state$ = null
      const output$ = epics.avatarUpdatingTimeoutEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('----', {})
    })
  })
})

describe('gameLoadedIntervalEpic', () => {
  it('it measure the time taken for the game to load and sends a corresponding analytic event', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('-------a-', {
        a: actions.gameDataLoaded()
      })

      const state$ = null
      const output$ = epics.gameLoadedInvteralEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('-------b-', {
        b: analyticActions.sendAnalyticsEvent('Kurono', 'Load', 'Game view', 7, true)
      })
    })
  })
})

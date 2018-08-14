/* eslint-env jest */
import { Observable, TestScheduler } from 'rxjs'
import { ActionsObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import configureStore from 'redux-mock-store'
import api from '../../api'
import { delay, mapTo } from 'rxjs/operators'
import { pipe } from 'rxjs/Rx'

const middlewares = []
const mockStore = configureStore(middlewares)

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
      return Observable.of(values.b)
    }

    const mockAPI = {
      api: {
        unity: {
          ...api.unity,
          emitToUnity: mockEmitToUnity
        }
      }
    }

    const actual = epics.sendGameStateEpic(source$, mockStore({}), mockAPI)

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
      return Observable.of(values.b)
    }

    const mockAPI = {
      api: {
        unity: {
          ...api.unity,
          emitToUnity: mockEmitToUnity

        }
      }
    }

    const actual = epics.sendAvatarIDEpic(source$, mockStore({}), mockAPI)

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
      mapTo({type: 'socket'})

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

    const actual = epics.connectToGameEpic(source$, mockStore({}), mockAPI)

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
      Observable.of({ avatar_id: 1 })

    const mockAPI = {
      api: {
        get: mockGetJSON
      }
    }

    const actual = epics.getConnectionParametersEpic(source$, mockStore({
      game: {
        connectionParameters: {
          game_id: 1
        }
      }
    }), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

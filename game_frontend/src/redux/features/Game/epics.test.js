/* eslint-env jest */
import { Observable, TestScheduler } from 'rxjs'
import { ActionsObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import configureStore from 'redux-mock-store'
import api from '../../api'
import { delay, mapTo, tap } from 'rxjs/operators'
import { pipe } from 'rxjs/Rx'

const middlewares = []
const mockStore = configureStore(middlewares)

const deepEquals = (actual, expected) =>
  expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('connectToGameEpic', () => {
  it('connects to the aimmo-game', () => {
    const gameState = {
      players: {
        id: 1,
        location: {
          x: 10,
          y: 10
        }
      }
    }

    const marbles1 = '-a---'
    const marbles2 = '--b--'
    const values = {
      a: actions.socketConnectToGameRequest(),
      b: actions.socketGameStateReceived(gameState)
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )
    const mockGetJSON = () =>
      Observable.of({ id: 1 })

    const mockConnectToGame = () =>
      mapTo({type: 'socket'})

    const mockStartListeners = () =>
      pipe(
        delay(10, testScheduler),
        mapTo(actions.socketGameStateReceived(gameState))
      )

    const mockAPI = {
      api: {
        get: mockGetJSON,
        socket: {
          connectToGame: mockConnectToGame,
          startListeners: mockStartListeners
        }
      }
    }

    const actual = epics.connectToGameEpic(source$, mockStore({
      game: {
        connectionParameters:
        {
          id: 1
        }
      }
    }), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

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

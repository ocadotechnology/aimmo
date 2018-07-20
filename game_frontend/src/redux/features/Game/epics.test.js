/* eslint-env jest */
import { Observable, TestScheduler } from 'rxjs'
import { ActionsObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import configureStore from 'redux-mock-store'
import api from '../../api'

const middlewares = []
const mockStore = configureStore(middlewares)

const deepEquals = (actual, expected) =>
  expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('getConnectionParametersEpic', () => {
  it('gets a ID connection param', () => {
    const gameIDRequested = 1
    const connectionParameters = {
      id: 1
    }

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.getConnectionParametersRequest(gameIDRequested),
      b: actions.getConnectionParametersSuccess(connectionParameters)
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )
    const mockGetJSON = () => {
      return Observable.of({id: connectionParameters.id})
    }

    const mockAPI = { api: { get: mockGetJSON } }

    const actual = epics.getConnectionParametersEpic(source$, mockStore({
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
      "pickups": [
        {
          "type": "invulnerability",
          "location": {
            "y": -6,
            "x": -6
          }
        },
      ],
      "obstacles": [
        {
          "orientation": "north",
          "width": 1,
          "type": "wall",
          "location": {
            "y": 9,
            "x": -7
          },
          "height": 1
        },
        {
          "orientation": "north",
          "width": 1,
          "type": "wall",
          "location": {
            "y": 4,
            "x": 9
          },
          "height": 1
        }
      ],
      "scoreLocations": [
        {
          "location": {
            "y": 10,
            "x": -15
          }
        }
      ],
      "players": [
        {
          "orientation": "north",
          "score": 0,
          "health": 5,
          "id": 1,
          "location": {
            "y": -1,
            "x": 14
          }
        }
      ],
      "northEastCorner": {
        "y": 15,
        "x": 15
      },
      "era": "less_flat",
      "southWestCorner": {
        "y": -15,
        "x": -15
      }
    }

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.socketGameStateReceived(gameState),
      b: actions.sendGameUpdateSuccess()
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

describe('establishGameConnection', () => {
  it('establishes the connection with the game', () => {
    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.establishGameConnection(),
      b: actions.establishGameConnectionSuccess()
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

    const actual = epics.establishGameConnectionEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

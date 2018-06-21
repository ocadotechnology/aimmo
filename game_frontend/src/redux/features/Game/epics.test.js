/* eslint-env jest */
import { Observable, TestScheduler } from 'rxjs'
import { ActionsObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import types from './types'
import configureStore from 'redux-mock-store'

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

describe('setGameURLEpic', () => {
  it('sets the game URL', () => {
    const gameURL = 'test'

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.setGameURL(gameURL),
      b: { type: types.SET_GAME_URL_SUCCESS }
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockSetGameURL = () => {
      return Observable.of('mockedUnityEvent')
    }

    const mockAPI = { api: { setGameURL: mockSetGameURL } }

    const actual = epics.setGameURLEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('setGamePath', () => {
  it('sets the game path', () => {
    const gamePath = 'test'

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.setGamePath(gamePath),
      b: { type: types.SET_GAME_PATH_SUCCESS }
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockSetGamePath = () => {
      return Observable.of('mockedUnityEvent')
    }

    const mockAPI = { api: { setGamePath: mockSetGamePath } }

    const actual = epics.setGamePathEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('setGamePort', () => {
  it('sets the game port', () => {
    const gamePort = 8000

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.setGamePort(gamePort),
      b: { type: types.SET_GAME_PORT_SUCCESS }
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockSetGamePort = () => {
      return Observable.of('mockedUnityEvent')
    }

    const mockAPI = { api: { setGamePort: mockSetGamePort } }

    const actual = epics.setGamePortEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('setGameSSL', () => {
  it('sets the game SSL flag', () => {
    const gameSSL = false

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.setGameSSL(gameSSL),
      b: { type: types.SET_GAME_SSL_SUCCESS }
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockSetGameSSL = () => {
      return Observable.of('mockedUnityEvent')
    }

    const mockAPI = { api: { setGameSSL: mockSetGameSSL } }

    const actual = epics.setGameSSLEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('establishGameConnection', () => {
  it('establishes the connection with the game', () => {
    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.establishGameConnection(),
      b: { type: types.ESTABLISH_GAME_CONNECTION_SUCCESS }
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockEstablishGameConnection = () => {
      return Observable.of('mockedUnityEvent')
    }

    const mockAPI = { api: { establishGameConnection: mockEstablishGameConnection } }

    const actual = epics.establishGameConnectionEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

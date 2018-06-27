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

describe('setGameURLEpic', () => {
  it('sets the game URL', () => {
    const gameURL = 'test'

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.setGameURL(gameURL),
      b: actions.setGameURLSuccess()
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

    const actual = epics.setGameURLEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('setGamePath', () => {
  it('sets the game path', () => {
    const gamePath = 'test'

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.setGamePath(gamePath),
      b: actions.setGamePathSuccess()
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

    const actual = epics.setGamePathEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('setGamePort', () => {
  it('sets the game port', () => {
    const gamePort = 8000

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.setGamePort(gamePort),
      b: actions.setGamePortSuccess()
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

    const actual = epics.setGamePortEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('setGameSSL', () => {
  it('sets the game SSL flag', () => {
    const gameSSL = false

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.setGameSSL(gameSSL),
      b: actions.setGameSSLSuccess()
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

    const actual = epics.setGameSSLEpic(source$, mockStore({}), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })

  it('catches the error and returns a fail action without completing the observable', () => {
    const gameSSL = false
    const error = new Error('Noooo!!')

    const marbles1 = '-a--'
    const marbles2 = '-b--'
    const values = {
      a: actions.setGameSSL(gameSSL),
      b: actions.setGameSSLFail(error)
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockEmitToUnity = () => {
      return Observable.throw(error)
    }

    const mockAPI = {
      api: {
        unity: {
          ...api.unity,
          emitToUnity: mockEmitToUnity
        }
      }
    }

    const actual = epics.setGameSSLEpic(source$, mockStore({}), mockAPI)

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

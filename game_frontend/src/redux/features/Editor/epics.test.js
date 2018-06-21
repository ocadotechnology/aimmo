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

describe('getCodeEpic', () => {
  it('gets the code', () => {
    const code = 'class Avatar'

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.getCodeRequest(),
      b: actions.getCodeReceived(code)
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )
    const mockGetJSON = () => {
      return Observable.of({ code })
    }

    const mockAPI = { api: { get: mockGetJSON } }

    const actual = epics.getCodeEpic(source$, mockStore(
      { game:
        { connectionParameters:
          { id: 1 }
        }
      }), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('postCodeEpic', () => {
  it('posts the code', () => {
    const code = 'class Avatar'

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.postCodeRequest(),
      b: actions.postCodeReceived()
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const mockPost = (url, body) => action$ => action$.mapTo({})
    const mockAPI = { api: { post: mockPost } }

    const state = {
      game: {
        connectionParameters: {
          id: 1
        }
      },
      editor: {
        code: code
      }
    }

    const actual = epics.postCodeEpic(source$, mockStore(state), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })

  it('catches an error', () => {
    const code = 'class Avatar'

    const marbles1 = '-a-'
    const marbles2 = '-(b|)-'
    const values = {
      a: actions.postCodeRequest(),
      b: {
        type: types.POST_CODE_FAILURE,
        payload: 'oh no!',
        error: true
      }
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )

    const error = { xhr: { response: 'oh no!' } }
    const mockPost = (url, body) => action$ => action$.mergeMapTo(Observable.throw(error))
    const mockAPI = { api: { post: mockPost } }

    const state = {
      game: {
        connectionParameters: {
          id: 1
        }
      },
      editor: {
        code: code
      }
    }

    const actual = epics.postCodeEpic(source$, mockStore(state), mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

describe('changeCodeEpic', () => {
  it('makes sure the state is not constantly updating due to changes in the editor', () => {
    const sourceMarbles = '-a-a--------'
    const expectMarbles = '---------b--'

    const values = {
      a: actions.keyPressed(''),
      b: actions.changeCode('')
    }

    const testScheduler = createTestScheduler(50)
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(sourceMarbles, values)
    )

    const actual = epics.changeCodeEpic(source$, mockStore({}), {}, testScheduler)

    testScheduler.expectObservable(actual).toBe(expectMarbles, values)
    testScheduler.flush()
  })
})

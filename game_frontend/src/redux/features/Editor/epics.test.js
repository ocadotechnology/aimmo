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

const createTestScheduler = () =>
  new TestScheduler(deepEquals)

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

    const actual = epics.getCodeEpic(source$, mockStore({game: { id: 1 }}), mockAPI)

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
        id: 1
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
        id: 1
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
  it('Only changes code after a certain amount of time', () => {
    const expectMarbles = '-a--------a----|'
    const actualMarbles = '-----b---------(b|)'

    const values = {
      a: actions.editorChanged(''),
      b: actions.changeCode('')
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(
      testScheduler.createColdObservable(expectMarbles, values)
    )

    const actual = epics.changeCodeEpic(source$)

    testScheduler.expectObservable(actual).toBe(actualMarbles, values)
    testScheduler.flush()
  })
})

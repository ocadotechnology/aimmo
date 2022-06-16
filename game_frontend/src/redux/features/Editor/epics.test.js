/* eslint-env jest */
import { of, throwError, Subject } from 'rxjs'
import { mapTo, mergeMapTo } from 'rxjs/operators'
import { TestScheduler } from 'rxjs/testing'
import { ActionsObservable, StateObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
import types from './types'

const deepEquals = (actual, expected) => expect(actual).toEqual(expected)

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
      b: actions.getCodeReceived(code),
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(testScheduler.createColdObservable(marbles1, values))
    const mockGetJSON = () => {
      return of({ code })
    }

    const mockAPI = { api: { get: mockGetJSON } }

    const initialState = {
      game: {
        connectionParameters: {
          id: 1,
        },
      },
    }
    const state$ = new StateObservable(new Subject(), initialState)

    const actual = epics.getCodeEpic(source$, state$, mockAPI)

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
      b: actions.postCodeReceived(),
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(testScheduler.createColdObservable(marbles1, values))

    const mockPost = (url, body) => (action$) => action$.pipe(mapTo({}))
    const mockAPI = { api: { post: mockPost } }

    const initialState = {
      game: {
        connectionParameters: {
          id: 1,
        },
      },
      editor: {
        code: { code },
      },
    }

    const state$ = new StateObservable(new Subject(), initialState)

    const actual = epics.postCodeEpic(source$, state$, mockAPI)

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
        error: true,
      },
    }

    const testScheduler = createTestScheduler()
    const source$ = ActionsObservable.from(testScheduler.createColdObservable(marbles1, values))

    const error = { xhr: { response: 'oh no!' } }
    const mockPost = (url, body) => (action$) => action$.pipe(mergeMapTo(throwError(error)))
    const mockAPI = { api: { post: mockPost } }

    const initialState = {
      game: {
        connectionParameters: {
          id: 1,
        },
      },
      editor: {
        code: code,
      },
    }
    const state$ = new StateObservable(new Subject(), initialState)

    const actual = epics.postCodeEpic(source$, state$, mockAPI)

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

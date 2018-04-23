/* eslint-env jest */
import { Observable, TestScheduler } from 'rxjs'
import { ActionsObservable } from 'redux-observable'
import epics from './epics'
import actions from './actions'
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
    const source = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )
    const mockGetJSON = () => {
      return Observable.of({ code })
    }

    const actual = epics.getCodeEpic(source, mockStore({game: { id: 1 }}), { getJSON: mockGetJSON })

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
    const source = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )
    const mockPost = () => {
      return Observable.of({})
    }

    const state = {
      game: {
        id: 1
      },
      editor: {
        code: code
      }
    }

    const actual = epics.postCodeEpic(source, mockStore(state), { post: mockPost })

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

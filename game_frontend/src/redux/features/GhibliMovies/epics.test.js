/* eslint-env jest */
import { Observable } from 'rxjs'
import { TestScheduler } from 'rxjs/testing'
import { ActionsObservable } from 'redux-observable'
import fetchMoviesEpic from './epics'
import actions from './actions'

const deepEquals = (actual, expected) =>
  expect(actual).toEqual(expected)

const createTestScheduler = () =>
  new TestScheduler(deepEquals)

describe('fetchMoviesEpic', () => {
  it('fetches movies', () => {
    const movies = [
      {
        'title': 'Deetastic 5',
        'Director': 'Stan Dee'
      }
    ]

    const marbles1 = '-a-'
    const marbles2 = '-b-'
    const values = {
      a: actions.fetchMovies(),
      b: actions.receiveMovies(movies)
    }

    const testScheduler = createTestScheduler()
    const source = ActionsObservable.from(
      testScheduler.createColdObservable(marbles1, values)
    )
    const mockGetJSON = () => {
      return Observable.of(movies)
    }

    const actual = fetchMoviesEpic(source, null, { getJSON: mockGetJSON })

    testScheduler.expectObservable(actual).toBe(marbles2, values)
    testScheduler.flush()
  })
})

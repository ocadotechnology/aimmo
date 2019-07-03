/* eslint-env jest */
import epics from './epics'
import { TestScheduler } from 'rxjs/testing'
import { actions } from 'features/Analytics'
import ReactGA from 'react-ga'

const deepEquals = (actual, expected) =>
  expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('sendToGoogleAnalyticsEpic', () => {
  it('sends an event to google analytics correctly', () => {
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a--', {
        a: actions.sendAnalyticsEvent('Test Category', 'Test Action', 'Test Label')
      })

      const state$ = null
      const output$ = epics.sendToGoogleAnalyticsEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('--b--', {
        b: actions.analyticsEventSent()
      })
    })

    expect(ReactGA.testModeAPI.calls).toEqual([
      ['create', 'foo', 'auto'],
      ['send',
        {
          'eventAction': 'Test Action',
          'eventCategory': 'Test Category',
          'eventLabel': 'Test Label',
          'eventValue': 0,
          'hitType': 'event',
          'nonInteraction': false
        }]
    ])
  })
})

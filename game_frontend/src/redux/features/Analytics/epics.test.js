/* eslint-env jest */
import epics from './epics'
import * as index from './index'
import { TestScheduler } from 'rxjs/testing'
import { actions } from 'features/Analytics'
import ReactGA from 'react-ga'

index.hasAnalyticsCookiesConsent = jest.fn(() => true)

const deepEquals = (actual, expected) => expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('sendToGoogleAnalyticsEpic', () => {
  it('sends an event to google analytics correctly', () => {
    ReactGA.testModeAPI.resetCalls()
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a--', {
        a: actions.sendAnalyticsEvent('Test Category', 'Test Action', 'Test Label'),
      })

      const state$ = null
      const output$ = epics.sendToGoogleAnalyticsEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('--b--', {
        b: actions.analyticsEventSent(),
      })
    })

    expect(ReactGA.testModeAPI.calls).toEqual([
      [
        'send',
        {
          eventAction: 'Test Action',
          eventCategory: 'Test Category',
          eventLabel: 'Test Label',
          eventValue: 0,
          hitType: 'event',
          nonInteraction: false,
        },
      ],
    ])
  })
})

describe('sendToGoogleAnalyticsTimingEventEpic', () => {
  it('sends an event to google analytics correctly', () => {
    ReactGA.testModeAPI.resetCalls()
    const testScheduler = createTestScheduler()

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--a--', {
        a: actions.sendAnalyticsTimingEvent('Test Category', 'Test Action', 'Test Label', 5),
      })

      const state$ = null
      const output$ = epics.sendToGoogleAnalyticsTimingEventEpic(action$, state$, {}, testScheduler)

      expectObservable(output$).toBe('--b--', {
        b: actions.analyticsTimingEventSent(),
      })
    })

    expect(ReactGA.testModeAPI.calls).toEqual([
      [
        'send',
        {
          timingVar: 'Test Action',
          timingCategory: 'Test Category',
          timingLabel: 'Test Label',
          timingValue: 5,
          hitType: 'timing',
        },
      ],
    ])
  })
})

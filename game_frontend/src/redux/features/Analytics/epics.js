import types from './types'
import actions from './actions'
import { hasAnalyticsCookiesConsent } from './index'
import ReactGA from 'react-ga'
import { tap, mapTo, filter } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const sendToGoogleAnalyticsEpic = (action$) =>
  action$.pipe(
    ofType(types.SEND_ANALYTICS_EVENT),
    filter(hasAnalyticsCookiesConsent),
    tap((action) => ReactGA.event(action.payload)),
    mapTo(actions.analyticsEventSent())
  )

const sendToGoogleAnalyticsTimingEventEpic = (action$) =>
  action$.pipe(
    ofType(types.SEND_ANALYTICS_TIMING_EVENT),
    filter(hasAnalyticsCookiesConsent),
    tap((action) => ReactGA.timing(action.payload)),
    mapTo(actions.analyticsTimingEventSent())
  )

export default {
  sendToGoogleAnalyticsEpic,
  sendToGoogleAnalyticsTimingEventEpic,
}

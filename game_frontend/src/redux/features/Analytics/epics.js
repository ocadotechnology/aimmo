import types from './types'
import actions from './actions'
import ReactGA from 'react-ga'
import { tap, mapTo } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const sendToGoogleAnalyticsEpic = action$ =>
  action$.pipe(
    ofType(types.SEND_ANALYTICS_EVENT),
    tap(action =>
      ReactGA.event(action.payload)
    ),
    mapTo(actions.analyticsEventSent())
  )

export default {
  sendToGoogleAnalyticsEpic
}

import types from './types'

const sendAnalyticsEvent = (category, action, label = '', value = 0, nonInteraction = false) => ({
  type: types.SEND_ANALYTICS_EVENT,
  payload: {
    category,
    action,
    label,
    value,
    nonInteraction,
  },
})

const sendAnalyticsTimingEvent = (category, variable, label = '', value = 0) => ({
  type: types.SEND_ANALYTICS_TIMING_EVENT,
  payload: {
    category,
    variable,
    label,
    value,
  },
})

const analyticsEventSent = () => ({
  type: types.ANALYTICS_EVENT_SENT,
})

const analyticsTimingEventSent = () => ({
  type: types.ANALYTICS_TIMING_EVENT_SENT,
})

export default {
  sendAnalyticsEvent,
  analyticsEventSent,
  analyticsTimingEventSent,
  sendAnalyticsTimingEvent,
}

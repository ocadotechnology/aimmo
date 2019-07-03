import types from './types'

const sendAnalyticsEvent = (category, action, label = '', value = 0, nonInteraction = false) => ({
  type: types.SEND_ANALYTICS_EVENT,
  payload: {
    category,
    action,
    label,
    value,
    nonInteraction
  }
})

const analyticsEventSent = () => ({
  type: types.ANALYTICS_EVENT_SENT
})

export default {
  sendAnalyticsEvent,
  analyticsEventSent
}

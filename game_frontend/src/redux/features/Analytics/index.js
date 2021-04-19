function hasAnalyticsCookiesConsent() {
  // C0002 is the Analytics Cookies category in OneTrust
  return !!window.OnetrustActiveGroups && window.OnetrustActiveGroups.split(',').includes('C0002')
}

export { hasAnalyticsCookiesConsent }
export { default as analyticTypes } from './types'
export { default as analyticEpics } from './epics'
export { default as actions } from './actions'

function hasAnalyticsCookiesConsent() {
  // CL002 is the Analytics Cookies category in OneTrust
  return !!window.OnetrustActiveGroups && window.OnetrustActiveGroups.split(',').includes('CL002')
}

export { hasAnalyticsCookiesConsent }
export { default as analyticTypes } from './types'
export { default as analyticEpics } from './epics'
export { default as actions } from './actions'

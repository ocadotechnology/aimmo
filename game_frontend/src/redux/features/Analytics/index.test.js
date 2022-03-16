import { hasAnalyticsCookiesConsent } from './index'

describe('hasAnalyticsCookiesConsent', () => {
  it('returns true when OnetrustActiveGroups contains analytics cookies consent', () => {
    window.OnetrustActiveGroups = 'CL001,CL002'
    expect(hasAnalyticsCookiesConsent()).toBe(true)
  })

  it('returns false when OnetrustActiveGroups is not set or does not contain analytics cookies consent', () => {
    window.OnetrustActiveGroups = undefined
    expect(hasAnalyticsCookiesConsent()).toBe(false)

    window.OnetrustActiveGroups = 'CL001,CL003'
    expect(hasAnalyticsCookiesConsent()).toBe(false)
  })
})

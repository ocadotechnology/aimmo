import { hasAnalyticsCookiesConsent } from './index'

describe('hasAnalyticsCookiesConsent', () => {
  it('returns true when OnetrustActiveGroups contains analytics cookies consent', () => {
    window.OnetrustActiveGroups = 'C0001,C0002'
    expect(hasAnalyticsCookiesConsent()).toBe(true)
  })

  it('returns false when OnetrustActiveGroups is not set or does not contain analytics cookies consent', () => {
    window.OnetrustActiveGroups = undefined
    expect(hasAnalyticsCookiesConsent()).toBe(false)

    window.OnetrustActiveGroups = 'C0001,C0003'
    expect(hasAnalyticsCookiesConsent()).toBe(false)
  })
})

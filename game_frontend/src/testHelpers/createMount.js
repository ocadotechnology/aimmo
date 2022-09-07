import React from 'react'
import PropTypes from 'prop-types'
import { ThemeProvider } from 'styled-components'
import { createMount } from '@material-ui/core/test-utils'
import themeVariants from 'theme'

const ThemeProviderWrapper = ({ children, theme }) => (
  <ThemeProvider theme={theme}>{children}</ThemeProvider>
)

ThemeProviderWrapper.propTypes = {
  children: PropTypes.component,
  theme: PropTypes.object,
}

/**
 * Creates a component using the given vairant of our theme. this renders the component in a "headless browser",
 * meaning that component specific functionality like mounting will occur when calling this function.
 * @param {React.component} component
 * @param {string} themeVariant
 * @param {boolean} dive
 */
export default function createMountWithTheme(component, themeVariant = 'light', dive = false) {
  return createMount({ dive })(component, {
    wrappingComponent: ThemeProviderWrapper,
    wrappingComponentProps: { theme: themeVariants[themeVariant] },
  })
}

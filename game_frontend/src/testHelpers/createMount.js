import React from 'react'
import { createShallow, createMount } from '@material-ui/core/test-utils'
import themeVariants from 'theme'
import { ThemeProvider } from 'styled-components'

/**
 * Creates a component using the given vairant of our theme. this renders the component in a "headless browser",
 * meaning that component specific functionality like mounting will occur when calling this function.
 * @param {React.component} component
 * @param {string} themeVariant
 * @param {boolean} dive
 */
export default function createMountWithTheme (component, themeVariant = 'light', dive = false) {
  const context = createShallow({ dive })(<ThemeProvider theme={themeVariants[themeVariant]} />)
    .instance()
    .getChildContext()

  return createMount({ dive })(component, {
    context,
    childContextTypes: ThemeProvider.childContextTypes
  })
}

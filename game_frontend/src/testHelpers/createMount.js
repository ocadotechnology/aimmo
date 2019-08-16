import React from 'react'
import { createShallow, createMount } from '@material-ui/core/test-utils'
import themeVariants from 'theme'
import { ThemeProvider } from 'styled-components'

export default function createMountWithTheme (component, themeVariant = 'light', dive = false) {
  const context = createShallow({ dive })(<ThemeProvider theme={themeVariants[themeVariant]} />)
    .instance()
    .getChildContext()

  return createMount({ dive })(component, {
    context,
    childContextTypes: ThemeProvider.childContextTypes
  }).instance()
}

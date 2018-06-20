import React from 'react'
import { createShallow } from '@material-ui/core/test-utils'
import theme from '../theme'
import { createMuiTheme } from '@material-ui/core/styles'

const muiTheme = createMuiTheme(theme)

export default function createShallowWithTheme (component) {
  return createShallow()(React.cloneElement(component, { theme: muiTheme }))
}

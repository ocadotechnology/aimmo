import React from 'react'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider } from 'styled-components'
import theme from '../theme'

const muiTheme = createMuiTheme(theme)

const withTheme = component => {
  return (
    <ThemeProvider theme={muiTheme}>
      <MuiThemeProvider theme={muiTheme}>
        {component}
      </MuiThemeProvider>
    </ThemeProvider>
  )
}

export default withTheme

import React, { Component } from 'react'
import IDEEditor from 'containers/IDEEditor'
import IDEConsole from 'containers/IDEConsole'
import { darkTheme } from 'theme'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'

export default class IDE extends Component {
  render () {
    return (
      <StyledComponentsThemeProvider theme={darkTheme}>
        <MuiThemeProvider theme={darkTheme}>
          <IDEEditor />
          <IDEConsole />
        </MuiThemeProvider>
      </StyledComponentsThemeProvider>
    )
  }
}

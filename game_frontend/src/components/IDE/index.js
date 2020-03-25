import React, { Component } from 'react'
import IDEEditor from 'containers/IDEEditor'
import IDEConsole from 'containers/IDEConsole'
import PropTypes from 'prop-types'
import { darkTheme } from 'theme'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'

export default class IDE extends Component {
  static propTypes = {
    logs: PropTypes.arrayOf(PropTypes.object)
  }

  render () {
    return (
      <StyledComponentsThemeProvider theme={darkTheme}>
        <MuiThemeProvider theme={darkTheme}>
          <IDEEditor />
          <IDEConsole logs={this.props.logs} />
        </MuiThemeProvider>
      </StyledComponentsThemeProvider>
    )
  }
}

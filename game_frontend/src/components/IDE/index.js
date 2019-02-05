import React, { Component } from 'react'
import IDEEditor from 'containers/IDEEditor'
import IDEConsole from 'containers/IDEConsole'
import PropTypes from 'prop-types'
import { darkTheme } from 'theme'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'

export default class IDE extends Component {
  static propTypes = {
    code: PropTypes.string,
    postCode: PropTypes.func,
    getCode: PropTypes.func,
    editorChanged: PropTypes.func,
    logs: PropTypes.arrayOf(PropTypes.object),
    runCodeButtonStatus: PropTypes.object
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

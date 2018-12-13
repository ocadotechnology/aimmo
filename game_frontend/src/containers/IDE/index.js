import React, { Component } from 'react'
import IDEEditor from 'components/IDEEditor'
import IDEConsole from 'components/IDEConsole'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { actions as editorActions } from 'features/Editor'
import { darkTheme } from 'theme'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'

export class IDE extends Component {
  render () {
    return (
      <StyledComponentsThemeProvider theme={darkTheme}>
        <MuiThemeProvider theme={darkTheme}>
          <IDEEditor
            code={this.props.code}
            codeOnServer={this.props.codeOnServer}
            postCode={this.props.postCode}
            getCode={this.props.getCode}
            editorChanged={this.props.editorChanged}
            runCodeButtonStatus={this.props.runCodeButtonStatus}
          />
          <IDEConsole logs={this.props.logs} />
        </MuiThemeProvider>
      </StyledComponentsThemeProvider>
    )
  }
}

const mapStateToProps = state => ({
  code: state.editor.code.code,
  codeOnServer: state.editor.code.codeOnServer,
  logs: state.consoleLog.logs,
  runCodeButtonStatus: state.editor.runCodeButton
})

const mapDispatchToProps = {
  getCode: editorActions.getCodeRequest,
  editorChanged: editorActions.keyPressed,
  postCode: editorActions.postCodeRequest
}

IDE.propTypes = {
  code: PropTypes.string,
  postCode: PropTypes.func,
  getCode: PropTypes.func,
  editorChanged: PropTypes.func,
  logs: PropTypes.arrayOf(PropTypes.object),
  runCodeButtonStatus: PropTypes.object
}

export default connect(mapStateToProps, mapDispatchToProps)(IDE)

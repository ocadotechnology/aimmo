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
  static propTypes = {
    code: PropTypes.string,
    postCode: PropTypes.func,
    getCode: PropTypes.func,
    editorChanged: PropTypes.func,
    logs: PropTypes.arrayOf(PropTypes.object)
  }

  render () {
    return (
      <StyledComponentsThemeProvider theme={darkTheme}>
        <MuiThemeProvider theme={darkTheme}>
          <IDEEditor
            code={this.props.code}
            postCode={this.props.postCode}
            getCode={this.props.getCode}
            editorChanged={this.props.editorChanged}
            avatarUpdating={this.props.avatarUpdating}
          />
          <IDEConsole logs={this.props.logs} />
        </MuiThemeProvider>
      </StyledComponentsThemeProvider>
    )
  }
}

const mapStateToProps = state => ({
  code: state.editor.code,
  logs: state.consoleLog.logs,
  avatarUpdating: state.game.avatarUpdating
})

const mapDispatchToProps = {
  getCode: editorActions.getCodeRequest,
  editorChanged: editorActions.keyPressed,
  postCode: editorActions.postCodeRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(IDE)

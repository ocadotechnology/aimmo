import React, { Component } from 'react'
import IDEEditor from 'components/IDEEditor'
import IDEConsole from 'components/IDEConsole'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { actions as editorActions } from 'features/Editor'
import ThemeProvider from 'components/ThemeProvider'

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
      <ThemeProvider variant='light'>
        <IDEEditor
          code={this.props.code}
          postCode={this.props.postCode}
          getCode={this.props.getCode}
          editorChanged={this.props.editorChanged}
        />
        <IDEConsole logs={this.props.logs} />
      </ThemeProvider>
    )
  }
}

const mapStateToProps = state => ({
  code: state.editor.code,
  logs: state.consoleLog.logs
})

const mapDispatchToProps = {
  getCode: editorActions.getCodeRequest,
  editorChanged: editorActions.keyPressed,
  postCode: editorActions.postCodeRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(IDE)

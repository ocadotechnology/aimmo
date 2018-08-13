import React, { Component, Fragment } from 'react'
import IDEMenu from 'components/IDEMenu'
import IDEEditor from 'components/IDEEditor'
import IDEConsole from 'components/IDEConsole'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { actions as editorActions } from 'features/Editor'

export class IDE extends Component {
  render () {
    return (
      <Fragment>
        <IDEMenu postCode={this.props.postCode} />
        <IDEEditor
          code={this.props.code}
          getCode={this.props.getCode}
          editorChanged={this.props.editorChanged}
        />
        <IDEConsole logs={this.props.logs} />
      </Fragment>
    )
  }
}

IDE.propTypes = {
  code: PropTypes.string,
  postCode: PropTypes.func,
  getCode: PropTypes.func,
  editorChanged: PropTypes.func,
  logs: PropTypes.arrayOf(PropTypes.object)
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

import styled from 'styled-components'
import React, { Component } from 'react'
import AceEditor from 'react-ace'
import 'brace/theme/idle_fingers'
import { connect } from 'react-redux'
import { actions } from 'features/Editor'
import PropTypes from 'prop-types'

const IDEEditorLayout = styled.div`
  background-color: #2F4F4F
  grid-area: ide-editor
`

export class IDEEditor extends Component {

  render () {
    return (
      <IDEEditorLayout>
        <AceEditor
          mode='javascript'
          theme='idle_fingers'
          name='ace_editor'
          onLoad={this.props.getCode}
          onChange={this.onChange}
          fontSize={14}
          showPrintMargin
          showGutter
          highlightActiveLine
          value={this.props.code}
          width='100%'
          height='100%'
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: false,
            showLineNumbers: true,
            tabSize: 2
          }} />
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  code: PropTypes.string,
  getCode: PropTypes.func,
  postCode: PropTypes.func
}

const mapStateToProps = state => {
  return {
    code: state.editor.code
  }
}

const mapDispatchToProps = {
  getCode: actions.getCodeRequest,
  postCode: actions.postCodeRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(IDEEditor)

import styled from 'styled-components'
import React, { Component } from 'react'
import AceEditor from 'react-ace'
import 'brace/theme/idle_fingers'
import 'brace/mode/python'
import 'brace/snippets/python'
import 'brace/ext/language_tools'
import { connect } from 'react-redux'
import { actions } from 'features/Editor'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'

export const IDEEditorLayout = styled.div`
  background-color: #2F4F4F
  grid-area: ide-editor
`
export class IDEEditor extends Component {
  render () {
    return (
      <IDEEditorLayout>
        <AceEditor
          mode='python'
          theme='idle_fingers'
          name='ace_editor'
          onLoad={this.props.getCode}
          onChange={this.props.editorChanged}
          fontSize={this.props.theme.additionalVariables.typography.code.fontSize}
          showPrintMargin
          showGutter
          highlightActiveLine
          value={this.props.code}
          width='100%'
          height='100%'
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: true,
            showLineNumbers: true,
            tabSize: 2,
            fontFamily: this.props.theme.additionalVariables.typography.code.fontFamily
          }} />
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  code: PropTypes.string,
  getCode: PropTypes.func,
  editorChanged: PropTypes.func,
  theme: PropTypes.object
}

const mapStateToProps = state => ({
  code: state.editor.code
})

const mapDispatchToProps = {
  getCode: actions.getCodeRequest,
  editorChanged: actions.keyPressed
}

export default connect(mapStateToProps, mapDispatchToProps)(withTheme()(IDEEditor))

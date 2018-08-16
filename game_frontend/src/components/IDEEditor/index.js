import styled from 'styled-components'
import React, { PureComponent } from 'react'
import AceEditor from 'react-ace'
import 'brace/theme/idle_fingers'
import 'brace/mode/python'
import 'brace/snippets/python'
import 'brace/ext/language_tools'
import { actions } from 'features/Editor'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import PlayIcon from '../icons/Play.js'
export const IDEEditorLayout = styled.div`
  background-color: #2F4F4F;
  position: relative;
  grid-area: ide-editor;
`
const FAB = styled(Button)`
  position: absolute !important;
  right: 20px;
  bottom: 15px;
  z-index: 5;
`
const MarginedPlayIcon = styled(PlayIcon)`
  margin-right: ${props => props.theme.spacing.unit}px;
`
export class IDEEditor extends PureComponent {
  render() {
    console.log(this.props.postCode)
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
        <FAB
            variant='extendedFab'
            id='post-code-button'
            onClick={this.props.postCode}>
            <MarginedPlayIcon />Post Code
        </FAB>
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  code: PropTypes.string,
  getCode: PropTypes.func,
  editorChanged: PropTypes.func,
  theme: PropTypes.object,
  postCode: PropTypes.func
}

export default withTheme()(IDEEditor)

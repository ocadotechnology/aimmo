import styled from 'styled-components'
import React, { PureComponent } from 'react'
import AceEditor from 'react-ace'
import 'brace/theme/idle_fingers'
import 'brace/mode/python'
import 'brace/snippets/python'
import 'brace/ext/language_tools'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import PlayIcon from 'components/icons/Play'

export const IDEEditorLayout = styled.div`
  position: relative;
  grid-area: ide-editor;
`

export const RunCodeButton = styled(Button)`
  && {
    position: absolute;
    right: ${props => props.theme.spacing.unit * 3}px;
    bottom: ${props => props.theme.spacing.unit * 3}px;
    z-index: 5;
  }
`

export const MarginedPlayIcon = styled(PlayIcon)`
  margin-right: ${props => props.theme.spacing.unit}px;
`

export class IDEEditor extends PureComponent {
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
        <RunCodeButton
          aria-label='Run Code'
          variant='extendedFab'
          id='post-code-button'
          onClick={this.props.postCode}>
          <MarginedPlayIcon />Run Code
        </RunCodeButton>
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

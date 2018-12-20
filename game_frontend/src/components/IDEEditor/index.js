import styled from 'styled-components'
import React, { PureComponent } from 'react'
import AceEditor from 'react-ace'
import 'brace/theme/idle_fingers'
import 'brace/mode/python'
import 'brace/snippets/python'
import 'brace/ext/language_tools'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'
import RunCodeButton from 'components/RunCodeButton'

export const IDEEditorLayout = styled.div`
  position: relative;
  grid-area: ide-editor;
`

export const PositionedRunCodeButton = styled(RunCodeButton)`
  && {
    position: absolute;
    right: ${props => props.theme.spacing.unit * 3}px;
    bottom: ${props => props.theme.spacing.unit * 3}px;
    z-index: 5;
  }
`

export class IDEEditor extends PureComponent {
  isCodeOnServerDifferent () {
    return this.props.code !== this.props.codeOnServer
  }

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
        <PositionedRunCodeButton
          runCodeButtonStatus={this.props.runCodeButtonStatus}
          isCodeOnServerDifferent={this.isCodeOnServerDifferent()}
          aria-label='Run Code'
          id='post-code-button'
          whenClicked={this.props.postCode} />
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  code: PropTypes.string,
  codeOnServer: PropTypes.string,
  getCode: PropTypes.func,
  editorChanged: PropTypes.func,
  theme: PropTypes.object,
  postCode: PropTypes.func,
  runCodeButtonStatus: PropTypes.object
}

export default withTheme()(IDEEditor)

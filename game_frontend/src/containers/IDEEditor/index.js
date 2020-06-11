import styled from 'styled-components'
import React, { PureComponent } from 'react'
import AceEditor from 'react-ace'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'
import RunCodeButton from 'components/RunCodeButton'
import { connect } from 'react-redux'
import { actions as editorActions } from 'features/Editor'

import 'ace-builds/src-noconflict/theme-solarized_dark'
import 'ace-builds/src-noconflict/mode-python'

export const IDEEditorLayout = styled.div`
  position: relative;
  grid-area: ide-editor;
`

export const PositionedRunCodeButton = styled(RunCodeButton)`
  && {
    position: absolute;
    right: ${props => props.theme.spacing(3)}px;
    bottom: ${props => props.theme.spacing(3)}px;
    z-index: 5;
  }
`

export class IDEEditor extends PureComponent {
  state = {
    code: '',
    codeLoaded: false
  }

  componentDidMount () {
    this.props.getCode()
  }

  static getDerivedStateFromProps (props, state) {
    if (!state.codeLoaded && props.codeOnServer) {
      return {
        code: props.codeOnServer,
        codeLoaded: true
      }
    }
    return state
  }

  isCodeOnServerDifferent = () => {
    return this.state.code !== this.props.codeOnServer
  }

  options () {
    return {
      enableBasicAutocompletion: true,
      enableLiveAutocompletion: true,
      enableSnippets: true,
      showLineNumbers: true,
      tabSize: 4,
      fontFamily: this.props.theme.additionalVariables.typography.code.fontFamily
    }
  }

  postCode = () => {
    this.props.postCode(this.state.code)
  }

  codeChanged = code => {
    this.setState({ code })
  }

  renderEditor () {
    if (this.state.codeLoaded) {
      return (
        <AceEditor
          mode='python'
          theme='solarized_dark'
          name='ace_editor'
          // onLoad={this.props.getCode}
          onChange={this.codeChanged}
          fontSize={this.props.theme.additionalVariables.typography.code.fontSize}
          showPrintMargin
          showGutter
          highlightActiveLine
          // debounceChangePeriod={300}
          value={this.state.code}
          width='100%'
          height='100%'
          setOptions={this.options()}
        />
      )
    }
  }

  render () {
    return (
      <IDEEditorLayout>
        {this.renderEditor()}
        <PositionedRunCodeButton
          runCodeButtonStatus={this.props.runCodeButtonStatus}
          isCodeOnServerDifferent={this.isCodeOnServerDifferent()}
          aria-label='Run Code'
          id='post-code-button'
          whenClicked={this.postCode}
        />
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  codeOnServer: PropTypes.string,
  getCode: PropTypes.func,
  codeChanged: PropTypes.func,
  theme: PropTypes.object,
  postCode: PropTypes.func,
  runCodeButtonStatus: PropTypes.object
}

const mapStateToProps = state => ({
  codeOnServer: state.editor.code.codeOnServer,
  runCodeButtonStatus: state.editor.runCodeButton
})

const mapDispatchToProps = {
  getCode: editorActions.getCodeRequest,
  codeChanged: editorActions.changeCode,
  postCode: editorActions.postCodeRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(withTheme(IDEEditor))

import styled from 'styled-components'
import React, { PureComponent } from 'react'
import AceEditor from 'react-ace'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'
import RunCodeButton from 'components/RunCodeButton'
import { connect } from 'react-redux'
import { actions as editorActions } from 'features/Editor'
import { PauseCircleFilled, SettingsBackupRestore } from '@material-ui/icons'

import 'ace-builds/src-noconflict/mode-python'
// The monokai theme is modified and overridden, see handlebars_template.html
import 'ace-builds/src-noconflict/theme-monokai'
import { Button } from '@material-ui/core'

export const IDEEditorLayout = styled.div`
  position: relative;
  grid-area: ide-editor;
`

export const MenuBar = styled.div`
  background: #2f3129;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  z-index: 10;
  padding: 0.5rem 1.5rem 0.5rem 0rem;
  gap: 1rem;
  height: 12%;
`

export const MenuButton = styled(Button)`
  border: none;
  height: 48px;
`

export class IDEEditor extends PureComponent {
  static propTypes = {
    codeOnServer: PropTypes.string,
    getCode: PropTypes.func,
    resetCode: PropTypes.func,
    resetCodeTo: PropTypes.string,
    codeReset: PropTypes.func,
    theme: PropTypes.object,
    postCode: PropTypes.func,
    runCodeButtonStatus: PropTypes.object,
  }

  state = {
    code: '',
    codeLoaded: false,
  }

  componentDidMount() {
    this.props.getCode()
  }

  static getDerivedStateFromProps(props, state) {
    if (!state.codeLoaded && props.codeOnServer) {
      return {
        code: props.codeOnServer,
        codeLoaded: true,
      }
    } else if (props.resetCodeTo) {
      const derivedState = {
        ...state,
        code: props.resetCodeTo,
      }
      props.codeReset()
      return derivedState
    }
    return state
  }

  isCodeOnServerDifferent = () => {
    return this.state.code !== this.props.codeOnServer
  }

  options() {
    return {
      showLineNumbers: true,
      tabSize: 4,
      fontFamily: this.props.theme.additionalVariables.typography.code.fontFamily,
    }
  }

  postCode = () => {
    this.props.postCode(this.state.code)
  }

  codeChanged = (code) => {
    this.setState({ code })
  }

  renderEditor() {
    if (this.state.codeLoaded) {
      return (
        <AceEditor
          mode="python"
          theme="monokai"
          name="ace_editor"
          onChange={this.codeChanged}
          fontSize="18px"
          showPrintMargin
          showGutter
          highlightActiveLine
          value={this.state.code}
          width="100%"
          height="88%"
          setOptions={this.options()}
        />
      )
    }
  }

  onResetCodeClicked = () => {
    if (confirm('Are you sure you want to reset to the starter code?')) {
      this.props.resetCode()
    }
  }

  render() {
    return (
      <IDEEditorLayout>
        {this.renderEditor()}
        <MenuBar>
          <MenuButton
            variant="outlined"
            onClick={this.onResetCodeClicked}
            startIcon={<SettingsBackupRestore />}
          >
            Reset code
          </MenuButton>
          <MenuButton variant="outlined" startIcon={<PauseCircleFilled />}>
            Pause
          </MenuButton>
          <RunCodeButton
            runCodeButtonStatus={this.props.runCodeButtonStatus}
            isCodeOnServerDifferent={this.isCodeOnServerDifferent()}
            aria-label="Run Code"
            id="post-code-button"
            whenClicked={this.postCode}
          />
        </MenuBar>
      </IDEEditorLayout>
    )
  }
}

const mapStateToProps = (state) => ({
  codeOnServer: state.editor.code.codeOnServer,
  resetCodeTo: state.editor.code.resetCodeTo,
  runCodeButtonStatus: state.editor.runCodeButton,
})

const mapDispatchToProps = {
  getCode: editorActions.getCodeRequest,
  codeReset: editorActions.codeReset,
  postCode: editorActions.postCodeRequest,
  resetCode: editorActions.resetCode,
}

export default connect(mapStateToProps, mapDispatchToProps)(withTheme(IDEEditor))

import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LogEntries from 'components/LogEntries'
import ConsoleBar from 'components/ConsoleBar'
import { connect } from 'react-redux'
import { actions } from 'redux/features/ConsoleLog'
import { actions as editorActions } from 'redux/features/Editor'

export const IDEConsoleSection = styled.section`
  grid-area: ide-console;
  display: flex;
  flex-direction: column;
`

export const StyledConsole = styled.div`
  color: ${props => props.theme.palette.text.primary};
  background-color: ${props => props.theme.palette.background.default};
  font-family: ${props => props.theme.additionalVariables.typography.code.fontFamily};
  overflow: auto;
  white-space: pre-line;
  height: 100%;
  
  ::-webkit-scrollbar {
    background-color: ${props => props.theme.palette.divider};
  }

  ::-webkit-scrollbar-track {
    background: ${props => props.theme.palette.divider}; 
  }

  ::-webkit-scrollbar-thumb {
    background: ${props => props.theme.palette.grey['A200']};
    border-radius: 100px;
    border: ${props => props.theme.spacing(0.25)}px solid transparent;
    background-clip: content-box;
  }
`

export class IDEConsole extends Component {
  static propTypes = {
    logs: PropTypes.arrayOf(PropTypes.object)
  }

  componentDidMount () {
    if (this.consoleRef) {
      this.consoleRef.scrollTo(0, 1)
    }
  }

  render () {
    return (
      <IDEConsoleSection>
        <ConsoleBar clearConsoleClicked={this.props.clearConsoleLogs} resetCodeClicked={this.props.resetCode} />
        <StyledConsole innerRef={ref => { this.consoleRef = ref }}>
          <LogEntries
            logs={this.props.logs}
          />
        </StyledConsole>
      </IDEConsoleSection>
    )
  }
}

const mapStateToProps = state => ({
  logs: state.consoleLog.logs
})

const mapDispatchToProps = {
  clearConsoleLogs: actions.clearConsoleLogs,
  resetCode: editorActions.resetCode
}

export default connect(mapStateToProps, mapDispatchToProps)(IDEConsole)

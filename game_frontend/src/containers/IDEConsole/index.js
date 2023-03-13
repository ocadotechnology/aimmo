import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LogEntries from 'components/LogEntries'
import ConsoleBar from 'components/ConsoleBar'
import { connect } from 'react-redux'
import { actions } from 'redux/features/ConsoleLog'
import ClearConsoleBar from 'components/ClearConsoleBar'

export const IDEConsoleSection = styled.section`
  grid-area: ide-console;
  display: flex;
  flex-direction: column;
`

export const StyledConsole = styled.div`
  color: ${(props) => props.theme.palette.text.primary};
  background-color: ${(props) => props.theme.palette.background.default};
  font-family: ${(props) => props.theme.additionalVariables.typography.code.fontFamily};
  overflow-y: auto;
  height: 100%;

  ::-webkit-scrollbar {
    background-color: ${(props) => props.theme.palette.divider};
  }

  ::-webkit-scrollbar-track {
    background: ${(props) => props.theme.palette.divider};
  }

  ::-webkit-scrollbar-thumb {
    background: ${(props) => props.theme.palette.grey.A200};
    border-radius: 100px;
    border: ${(props) => props.theme.spacing(0.25)}px solid transparent;
    background-clip: content-box;
  }
`

export class IDEConsole extends Component {
  static propTypes = {
    logs: PropTypes.instanceOf(Map),
    clearConsoleLogs: PropTypes.func,
  }

  // see https://blog.eqrion.net/pin-to-bottom/
  state = {
    activatedScrollToBottom: false,
    shouldActivateSnapToBottom: false,
  }

  componentDidUpdate() {
    this.snapToBottomIfNeeded()
  }

  isOverflown({ clientHeight, scrollHeight }) {
    return scrollHeight > clientHeight
  }

  isOverflownForTheFirstTime() {
    return (
      !this.state.activatedScrollToBottom && this.consoleRef && this.isOverflown(this.consoleRef)
    )
  }

  snapToBottomIfNeeded() {
    if (this.isOverflownForTheFirstTime()) {
      this.setState({
        ...this.state,
        shouldActivateSnapToBottom: true,
        activatedScrollToBottom: true,
      })
    } else if (this.state.activatedScrollToBottom && this.state.shouldActivateSnapToBottom) {
      this.setState({ ...this.state, shouldActivateSnapToBottom: false })
    }
  }

  clearConsole = () => {
    this.props.clearConsoleLogs()
    this.setState({ ...this.state, activatedScrollToBottom: false })
  }

  render() {
    return (
      <IDEConsoleSection>
        <ConsoleBar />
        <StyledConsole
          ref={(ref) => {
            this.consoleRef = ref
          }}
        >
          <LogEntries
            shouldActivateSnapToBottom={this.state.shouldActivateSnapToBottom}
            logs={this.props.logs}
          />
        </StyledConsole>
        <ClearConsoleBar clearConsoleClicked={this.clearConsole} />
      </IDEConsoleSection>
    )
  }
}

const mapStateToProps = (state) => ({
  logs: state.consoleLog.logs,
})

const mapDispatchToProps = {
  clearConsoleLogs: actions.clearConsoleLogs,
}

export default connect(mapStateToProps, mapDispatchToProps)(IDEConsole)

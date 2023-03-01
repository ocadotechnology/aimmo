import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LogEntries from 'components/LogEntries'
import ConsoleBar from 'components/ConsoleBar'
import { connect } from 'react-redux'
import { actions } from 'redux/features/ConsoleLog'
import { actions as editorActions } from 'redux/features/Editor'
import { actions as gameActions } from 'redux/features/Game'

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
    resetCode: PropTypes.func,
    clearConsoleLogs: PropTypes.func,
    togglePauseGame: PropTypes.func,
    gamePaused: PropTypes.bool,
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

  resetCode = () => {
    if (confirm('Are you sure you want to reset to the starter code?')) {
      this.props.resetCode()
    }
  }

  togglePauseGame = () => {
    this.props.togglePauseGame()
  }

  render() {
    return (
      <IDEConsoleSection>
        <ConsoleBar
          gamePaused={this.props.gamePaused}
          clearConsoleClicked={this.clearConsole}
          handleResetCodeClicked={this.resetCode}
          handlePauseGameClicked={this.togglePauseGame}
        />
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
      </IDEConsoleSection>
    )
  }
}

const mapStateToProps = (state) => ({
  logs: state.consoleLog.logs,
  gamePaused: state.game.gamePaused,
})

const mapDispatchToProps = {
  clearConsoleLogs: actions.clearConsoleLogs,
  resetCode: editorActions.resetCode,
  togglePauseGame: gameActions.togglePauseGame,
}

export default connect(mapStateToProps, mapDispatchToProps)(IDEConsole)

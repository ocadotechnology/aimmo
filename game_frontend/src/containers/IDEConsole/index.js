import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LogEntries from 'components/LogEntries'
import ConsoleBar from 'components/ConsoleBar'
import { connect } from 'react-redux'

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
    border: ${props => props.theme.spacing.unit / 4}px solid transparent;
    background-clip: content-box;
  }
`

export class IDEConsole extends Component {
  static propTypes = {
    logs: PropTypes.arrayOf(PropTypes.object)
  }

  state = {
    scrolledToBottom: true
  }

  handleScroll = event => {
    let target = event.target || event.srcElement
    this.setState({ ...this.state, scrolledToBottom: target.offsetHeight + target.scrollTop === target.scrollHeight })
  }

  componentDidMount () {
    if (this.consoleRef) {
      this.consoleRef.addEventListener('scroll', this.handleScroll)
    }
  }

  componentWillUnmount () {
    this.consoleRef.removeEventListener('scroll', this.handleScroll)
  }

  componentDidUpdate () {
    if (this.lastLogRef && this.state.scrolledToBottom) {
      this.lastLogRef.scrollIntoView(false)
    }
  }

  render () {
    return (
      <IDEConsoleSection>
        <ConsoleBar />
        <StyledConsole innerRef={ref => { this.consoleRef = ref }}>
          <LogEntries
            logs={this.props.logs}
            lastLogRef={ref => { this.lastLogRef = ref }} />
        </StyledConsole>
      </IDEConsoleSection>
    )
  }
}

const mapStateToProps = state => ({
  logs: state.consoleLog.logs
})

const mapDispatchToProps = {}

export default connect(mapStateToProps, mapDispatchToProps)(IDEConsole)

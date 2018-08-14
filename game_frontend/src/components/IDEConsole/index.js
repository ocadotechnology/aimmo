import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LogEntries from 'components/LogEntries'

export const StyledConsole = styled.div`
  grid-area: ide-console;
  color: ${props => props.theme.palette.text.primary};
  background-color: ${props => props.theme.palette.background.default};
  font-family: ${props => props.theme.additionalVariables.typography.code.fontFamily};
  overflow: auto;
  white-space: pre-line;
  padding-bottom: 0px;

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

export default class IDEConsole extends Component {
  state = {
    scrolledToBottom: true
  }

  handleScroll = event => {
    let srcElement = event.srcElement
    this.setState({...this.state, scrolledToBottom: srcElement.offsetHeight + srcElement.scrollTop === srcElement.scrollHeight})
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
      <StyledConsole innerRef={ref => { this.consoleRef = ref }}>
        <LogEntries
          logs={this.props.logs}
          lastLogRef={ref => { this.lastLogRef = ref }} />
      </StyledConsole>
    )
  }
}

IDEConsole.propTypes = {
  logs: PropTypes.arrayOf(PropTypes.object)
}

import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

export const LogEntry = styled.li`
  list-style: none;
  padding: ${props => props.theme.spacing.unit}px;
`

export const StyledLogEntries = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`

export default class LogEntries extends Component {
  generateLogEntries () {
    const lastLogEntry = this.props.logs[this.props.logs.length - 1]
    const logEntries = this.props.logs.map(logEntry =>
      <LogEntry
        key={logEntry.timestamp}
        innerRef={this.setLastLogEntryRef(logEntry, lastLogEntry)}>
        {logEntry.log}
      </LogEntry>
    )
    return logEntries
  }

  setLastLogEntryRef (logEntry, lastLogEntry) {
    return node => {
      if (logEntry.timestamp === lastLogEntry.timestamp) {
        this.props.lastLogRef(node)
      }
    }
  }

  render () {
    return (
      <StyledLogEntries>
        {this.generateLogEntries()}
      </StyledLogEntries>
    )
  }
}

LogEntries.propTypes = {
  logs: PropTypes.arrayOf(
    PropTypes.shape({
      timestamp: PropTypes.int,
      log: PropTypes.string
    })),
  lastLogRef: PropTypes.func
}

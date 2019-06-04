import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

export const LogEntry = styled.li`
  list-style: none;
  padding: ${props => props.theme.spacing()}px;
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
        key={logEntry.turn_count}
        innerRef={this.setLastLogEntryRef(logEntry, lastLogEntry)}>
        {logEntry.message}
      </LogEntry>
    )
    return logEntries
  }

  setLastLogEntryRef (logEntry, lastLogEntry) {
    return node => {
      if (logEntry.turn_count === lastLogEntry.turn_count) {
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
      turn_count: PropTypes.int,
      message: PropTypes.string
    })),
  lastLogRef: PropTypes.func
}

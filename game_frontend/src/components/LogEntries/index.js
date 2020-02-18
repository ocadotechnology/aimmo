import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

export const LogEntry = styled.li`
  list-style: none;
  padding: ${props => props.theme.spacing()}px;
  overflow-anchor: none;
`

export const BottomSnapper = styled.li`
  overflow-anchor: auto;
  height: 1px;
  list-style: none;
`

export const StyledLogEntries = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`

export default class LogEntries extends Component {
  generateLogEntries () {
    let logEntries = this.props.logs.map(logEntry => (
      <LogEntry key={logEntry.turn_count}>{logEntry.message}</LogEntry>
    ))
    logEntries.push(
      <BottomSnapper key={-1} />
    )
    return logEntries
  }

  render () {
    return <StyledLogEntries>{this.generateLogEntries()}</StyledLogEntries>
  }
}

LogEntries.propTypes = {
  logs: PropTypes.arrayOf(
    PropTypes.shape({
      turn_count: PropTypes.int,
      message: PropTypes.string
    })
  )
}

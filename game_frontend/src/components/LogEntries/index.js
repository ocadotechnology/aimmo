import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableRow from '@material-ui/core/TableRow'

export const LogEntry = styled(TableRow)`
  overflow-anchor: none;
  font-family: ${props =>
    props.theme.additionalVariables.typography.code.fontFamily};
  font-size: ${props =>
    props.theme.additionalVariables.typography.code.fontSize};
`

export const LogData = styled(TableCell)`
  padding-inline-start: ${props => props.theme.spacing(3)}px;
`

export const LogTurn = styled(TableCell)`
  color: ${props => props.theme.palette.grey['500']};
  white-space: nowrap;
  vertical-align: text-top;
`

export const BottomSnapper = styled.tr`
  overflow-anchor: auto;
  height: 1px;
`

export const StyledTable = styled(Table)`
  white-space: pre-line;
`

export default class LogEntries extends Component {
  isOverflown ({ clientWidth, clientHeight, scrollWidth, scrollHeight }) {
    return scrollHeight > clientHeight || scrollWidth > clientWidth
  }

  componentDidUpdate () {
    if (this.bottomSnapperRef && this.props.shouldActivateSnapToBottom) {
      this.bottomSnapperRef.scrollIntoView({ behavior: 'smooth' })
    }
  }

  generateLogEntries () {
    const logEntries = this.props.logs.map(logEntry => (
      <LogEntry key={logEntry.turn_count}>
        <LogData>{logEntry.message}</LogData>
        <LogTurn align='right'>Turn: {logEntry.turn_count}</LogTurn>
      </LogEntry>
    ))
    logEntries.push(
      <BottomSnapper
        key={-1}
        innerRef={ref => {
          this.bottomSnapperRef = ref
        }}
      />
    )
    return logEntries
  }

  render () {
    return (
      <StyledTable size='small' innerRef={ref => { this.tableRef = ref }}>
        <TableBody>{this.generateLogEntries()}</TableBody>
      </StyledTable>
    )
  }
}

LogEntries.propTypes = {
  shouldActivateSnapToBottom: PropTypes.bool,
  logs: PropTypes.arrayOf(
    PropTypes.shape({
      turn_count: PropTypes.int,
      message: PropTypes.string
    })
  )
}

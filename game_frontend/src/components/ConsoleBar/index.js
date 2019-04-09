import styled from 'styled-components'
import Toolbar from '@material-ui/core/Toolbar/Toolbar'
import { Typography } from '@material-ui/core'
import ConsoleIcon from 'components/icons/Console'
import React, { Component } from 'react'

export const ClearToolbar = styled(Toolbar)`
  height: 40px;
  width: auto;
  background-color: ${props => props.theme.palette.grey['A700']};
`

export const StyledConsoleIcon = styled(ConsoleIcon)`
  padding-right: ${props => props.theme.spacing.unit}px;
`

export default class ConsoleBar extends Component {
  render () {
    return (
      <ClearToolbar variant='dense' >
        <StyledConsoleIcon color='disabled' />
        <Typography variant='body1' color='textSecondary'>Console Log</Typography>
      </ClearToolbar>
    )
  }
}

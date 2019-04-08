import styled from 'styled-components'
import Toolbar from '@material-ui/core/Toolbar/Toolbar'
import IconButton from '@material-ui/core/IconButton/IconButton'
import ClearIcon from 'components/icons/Clear'
import React, { Component } from 'react'
import { StyledConsole, StyledDiv } from '../../containers/IDEConsole'

export const ClearToolbar = styled(Toolbar)`
   background-color: ${props => props.theme.palette.grey['A700']};
  justify-content: flex-end;
`

export default class ConsoleBar extends Component {
  render () {
    return (
      <ClearToolbar>
        <IconButton
          aria-label='Clear'
          color='default'>
          <ClearIcon/>
        </IconButton>
      </ClearToolbar>
    )
  }
}
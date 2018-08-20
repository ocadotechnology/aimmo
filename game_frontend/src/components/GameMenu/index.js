import styled from 'styled-components'
import React, { Component } from 'react'
import IconButton from '@material-ui/core/IconButton'
import CloseIcon from '../icons/Close.js'

export const GameMenuLayout = styled.nav`
  background-color: ${props => props.theme.palette.background.default}
  grid-area: game-menu
`

export const ExitButton = styled(IconButton)`
  position: relative;
  float: right;
  right: ${props => props.theme.spacing.unit * 2}px;
  top: ${props => props.theme.spacing.unit * 2}px; 
`

export default class GameMenu extends Component {
  render () {
    return (
      <GameMenuLayout>
        <ExitButton href='/aimmo' aria-label='Close'>
          <CloseIcon />
        </ExitButton>
      </GameMenuLayout>
    )
  }
}

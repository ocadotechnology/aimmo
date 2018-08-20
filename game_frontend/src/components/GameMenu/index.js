import styled from 'styled-components'
import React, { Component } from 'react'
import IconButton from '@material-ui/core/IconButton'
import CloseIcon from '../icons/Close.js'

const GameMenuLayout = styled.nav`
  background-color: ${props => props.theme.palette.background.default}
  grid-area: game-menu
`

const ExitButton = styled(IconButton)`
  position: relative;
  float: right;
  right: 40px;
  top: 20px;
`

export default class GameMenu extends Component {
  render () {
    return (
      <GameMenuLayout>
        <a href='/aimmo'>
          <ExitButton aria-label='Close'>
            <CloseIcon />
          </ExitButton>
        </a>
      </GameMenuLayout>
    )
  }
}

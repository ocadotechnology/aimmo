import styled from 'styled-components'
import React, { Component } from 'react'
import Button from '@material-ui/core/Button'
import CloseIcon from '../icons/Close.js'

const GameMenuLayout = styled.nav`
  background-color: ${props => props.theme.palette.background.default}
  grid-area: game-menu
`

const ExitButton = styled(Button)`
  position: relative;
  float: right;
  right: 40px;
  top: 20px;
`

export default class GameMenu extends Component {
  onClick () {
    const url = window.location.href
    window.location.href = url.substr(0, url.indexOf('play'))
  }
  render () {
    return (
      <GameMenuLayout>
        <ExitButton
          onClick={this.onClick.bind(this)}> <CloseIcon /> </ExitButton>
      </GameMenuLayout>
    )
  }
}

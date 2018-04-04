import React, { Component } from 'react'
import Menu from 'components/Menu'
import IDE from 'components/IDE'
import Game from 'components/Game'
import styled from 'styled-components'

const GamePageContainer = styled.div`
  display: grid
  grid-template: 80px 1fr 150px / 100px 1fr 1fr
  grid-template-areas: "menu ide-menu game-menu"
                       "menu ide-editor game-view"
                       "menu ide-console game-view";
  width: 100vw
  height: 100vh
`

export class GamePage extends Component {
  render () {
    return (
      <GamePageContainer>
        <Menu />
        <IDE />
        <Game />
      </GamePageContainer>
    )
  }
}

export default GamePage

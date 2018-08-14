import React, { Component } from 'react'
import styled from 'styled-components'
import IDE from 'containers/IDE'
import Game from 'components/Game'

export const GamePageLayout = styled.div`
  display: grid;
  grid-template: 80px 1fr 250px / 1fr 1fr;
  grid-template-areas: "ide-menu game-menu"
                       "ide-editor game-view"
                       "ide-console game-view";
  width: 100vw;
  height: 100vh;
`

export default class GamePage extends Component {
  render () {
    return (
      <GamePageLayout>
        <IDE />
        <Game />
      </GamePageLayout>
    )
  }
}

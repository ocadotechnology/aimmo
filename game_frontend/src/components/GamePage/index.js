import React, { Component } from 'react'
import styled from 'styled-components'
import IDE from 'components/IDE'
import Game from 'containers/Game'
import NavigationBar from 'components/NavigationBar'

export const GamePageLayout = styled.div`
  display: grid;
  grid-template: auto 1fr 290px / 1fr 1fr;
  grid-template-areas:
    'navigation-bar navigation-bar'
    'ide-editor game-view'
    'ide-console game-view';
  width: 100vw;
  height: 100vh;
`

export default class GamePage extends Component {
  render() {
    return (
      <GamePageLayout>
        <NavigationBar />
        <IDE />
        <Game />
      </GamePageLayout>
    )
  }
}

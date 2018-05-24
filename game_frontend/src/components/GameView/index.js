import styled from 'styled-components'
import React, { Component } from 'react'
import Unity from "react-unity-webgl"

const GameViewLayout = styled.div`
  background-color: purple
  grid-area: game-view
`

export class GameView extends Component {
  render() {
    return (
      <GameViewLayout>
        <Unity
          src="TODO"
          loader="TODO"
        />
      </GameViewLayout>
    )
  }
}
export default GameView

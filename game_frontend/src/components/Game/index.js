import styled from 'styled-components'
import React, { Component, Fragment } from 'react'

export const GameMenu = styled.nav`
  background-color: pink
  grid-area: game-menu
`

export const GameView = styled.div`
  background-color: purple
  grid-area: game-view
`

export default class Game extends Component {
  render () {
    return (
      <Fragment>
        <GameMenu />
        <GameView />
      </Fragment>
    )
  }
}

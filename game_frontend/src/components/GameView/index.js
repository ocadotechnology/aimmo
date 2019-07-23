import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export default class GameView extends Component {
  render () {
    return (
      <GameViewLayout />
    )
  }
}

GameView.propTypes = {
  connectToGame: PropTypes.func,
  gameDataLoaded: PropTypes.bool
}

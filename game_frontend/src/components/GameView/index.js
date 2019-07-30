import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Environment from '../../babylon/environment'
import EntityManager from '../../babylon/entities'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export default class GameView extends Component {
  constructor(props) {
    super(props)
    this.props.connectToGame()
  }

  componentDidMount() {
    this.environment = new Environment(this.canvas)
    this.environment.setup()
    this.entities = new EntityManager(this.environment)
    this.entities.setup()

    // Resize the babylon engine when the window is resized
    window.addEventListener('resize', this.environment.windowResized)
  }

  componentDidUpdate(prevProps) {
    this.entities.onGameStateUpdate(prevProps.gameState, this.props.gameState)
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.environment.windowResized)
  }

  onCanvasLoaded = canvas => {
    if (canvas !== null) {
      this.canvas = canvas
    }
  }

  render() {
    return (
      <GameViewLayout>
        <canvas
          style={{ width: '100%', height: '100%' }}
          ref={this.onCanvasLoaded}
        />
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  connectToGame: PropTypes.func,
  gameDataLoaded: PropTypes.bool,
  gameState: PropTypes.object
}

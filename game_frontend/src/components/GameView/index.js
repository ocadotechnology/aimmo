import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Environment from '../../babylon/environment'
import Entities from '../../babylon/entities'

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
    this.entities = new Entities(this.canvas, this.environment.engine, this.environment.scene)
    this.entities.onSceneMount()

    // Resize the babylon engine when the window is resized
    window.addEventListener('resize', this.environment.windowResized)
  }

  componentDidUpdate() {
    if (this.props.gameState) {
      this.entities.onGameStateUpdate(this.props.gameState, this.environment.terrain.onTerrainNode)
    }
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

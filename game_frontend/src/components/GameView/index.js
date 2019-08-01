import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import EntityManager from '../../babylon/entities'
import SceneRenderer from '../../babylon/environment'
import EnvironmentManager from '../../babylon/environment/environmentManager'
import Environment from '../../babylon/environment/environment'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export const Compass = styled.img`
  position: absolute;
  bottom: 1%;
  left: 51%;
  z-index: 100000;
`

export default class GameView extends Component {
  constructor(props) {
    super(props)
    this.props.connectToGame()
  }
  
  componentDidMount() {
    this.environment = new Environment(this.canvas)
    this.environment.setup()

    this.sceneRenderer = new SceneRenderer(this.environment)
    this.sceneRenderer.setup()

    this.environmentManager = new EnvironmentManager()
    this.environmentManager.setup(this.environment)

    this.entities = new EntityManager(this.environment)
    this.entities.setup()

    // Resize the babylon engine when the window is resized
    window.addEventListener('resize', this.sceneRenderer.windowResized)
  }

  componentDidUpdate(prevProps) {
    this.entities.onGameStateUpdate(prevProps.gameState, this.props.gameState)
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.sceneRenderer.windowResized)
  }

  onCanvasLoaded = canvas => {
    if (canvas !== null) {
      this.canvas = canvas
    }
  }

  render() {
    return (
      <GameViewLayout>
        <Compass src="/static/images/compass.svg" />
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

import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import EntityManager from '../../babylon/entities'
import SceneRenderer from '../../babylon/environment'
import EnvironmentManager from '../../babylon/environment/environmentManager'
import { StandardEnvironment } from '../../babylon/environment/environment'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export const Compass = styled.img`
  position: sticky;
  bottom: ${props => props.theme.spacing()}px;
  padding-left: ${props => props.theme.spacing()}px;
`

export default class GameView extends Component {
  constructor (props) {
    super(props)
    this.props.connectToGame()
  }

  componentDidMount () {
    this.environment = new StandardEnvironment(this.canvas)
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

  componentDidUpdate (prevProps) {
    this.entities.onGameStateUpdate(prevProps.gameState, this.props.gameState)
  }

  componentWillUnmount () {
    window.removeEventListener('resize', this.sceneRenderer.windowResized)
  }

  onCanvasLoaded = canvas => {
    if (canvas !== null) {
      this.canvas = canvas
    }
  }

  render () {
    return (
      <GameViewLayout>
        <canvas
          style={{ width: '100%', height: '100%' }}
          ref={this.onCanvasLoaded}
        />
        <Compass src='/static/images/compass.svg' />
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  connectToGame: PropTypes.func,
  gameDataLoaded: PropTypes.bool,
  gameState: PropTypes.object
}

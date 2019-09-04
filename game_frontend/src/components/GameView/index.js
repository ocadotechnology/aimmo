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
  static propTypes = {
    connectToGame: PropTypes.func,
    gameState: PropTypes.object,
    currentAvatarID: PropTypes.number
  }

  constructor (props) {
    super(props)
    this.EnvironmentClass = this.props.EnvironmentClass ?? StandardEnvironment
  }

  componentDidMount () {
    this.setupGameEngine()
    this.props.connectToGame()
  }

  componentDidUpdate (prevProps) {
    this.updateGameState(prevProps)
    this.updateCurrentAvatarID(prevProps)
  }

  setupGameEngine () {
    this.environment = new this.EnvironmentClass(this.canvas)
    this.sceneRenderer = new SceneRenderer(this.environment)
    this.environmentManager = new EnvironmentManager(this.environment)
    this.entities = new EntityManager(this.environment)

    window.addEventListener('resize', this.environmentManager.resizeBabylonWindow)
  }

  updateGameState (prevProps) {
    if (this.props.gameState !== undefined) {
      this.entities.onGameStateUpdate(prevProps.gameState, this.props.gameState)
    }
  }

  updateCurrentAvatarID (prevProps) {
    if (prevProps.currentAvatarID !== this.props.currentAvatarID) {
      this.entities.setCurrentAvatarID(this.props.currentAvatarID)
    }
  }

  componentWillUnmount () {
    window.removeEventListener('resize', this.environmentManager.windowResized)
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

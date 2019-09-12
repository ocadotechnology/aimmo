import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import EntityManager from '../../babylon/entities'
import SceneRenderer from '../../babylon/environment'
import EnvironmentManager from '../../babylon/environment/environmentManager'
import { StandardEnvironment } from '../../babylon/environment/environment'
import { CircularProgress } from '@material-ui/core'
import Typography from '@material-ui/core/Typography'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export const LoadingBackgroundOverlay = styled.div`
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: ${props => props.theme.palette.primary.light};
`

export const LoadingText = styled(Typography)`
  padding-top: ${props => props.theme.spacing(2)}px;
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
    currentAvatarID: PropTypes.number,
    avatarReady: PropTypes.bool
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

  renderGameView = () => {
    return (
      <canvas
      style={{ width: '100%', height: '100%' }}
      ref={this.onCanvasLoaded}
      />
    )
  }

  render () {
    let loadingScreen = (
      <LoadingBackgroundOverlay>
          <CircularProgress color='inherit' />
          <LoadingText
            variant='body1'
            color='inherit'>
            Building game world...
          </LoadingText>
        </LoadingBackgroundOverlay>
    )

    let compass = (
      <Compass src='/static/images/compass.svg' />
    )

    return (
      <GameViewLayout>
        {(!this.props.avatarReady) && loadingScreen}
        {this.renderGameView()}
        {this.props.avatarReady && compass}
      </GameViewLayout>
    )
  }
}

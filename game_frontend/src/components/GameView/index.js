import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { CircularProgress } from '@material-ui/core'
import Typography from '@material-ui/core/Typography'
import GameEngine from '../../babylon/gameEngine'
import { StandardEnvironment } from '../../babylon/environment/environment'

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
  background-color: ${props => props.theme.palette.primary.contrastText};
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
    gameLoaded: PropTypes.bool,
    cameraCenteredOnUserAvatar: PropTypes.bool,
    mapPanned: PropTypes.func
  }

  constructor (props) {
    super(props)
  }

  componentDidMount () {
    this.props.connectToGame()
    const environment = this.props.environment ?? new StandardEnvironment(this.canvas)
    this.gameEngine = new GameEngine(this.canvas, this.handleMapPanned, environment, this.props)
  }

  componentDidUpdate (prevProps) {
    this.gameEngine.onUpdate(prevProps, this.props)
  }

  componentWillUnmount () {
    this.gameEngine.unmount()
  }

  onCanvasLoaded = canvas => {
    if (canvas !== null) {
      this.canvas = canvas
    }
  }

  handleMapPanned = () => {
    this.props.mapPanned()
  }


  renderGameView = () => {
    return (
      <canvas
      style={{ width: '100%', height: '100%' }}
      ref={this.onCanvasLoaded}
      />
    )
  }

  renderLoadingScreen = () => {
    return (
      <LoadingBackgroundOverlay>
          <CircularProgress color='inherit' />
          <LoadingText
            variant='body1'
            color='inherit'>
            Building game world...
          </LoadingText>
        </LoadingBackgroundOverlay>
      )
  }

  renderCompass = () => {
    return (
      <Compass src='/static/images/compass.svg' />
    )
  }

  render () {
    return (
      <GameViewLayout>
        {!this.props.gameLoaded && this.renderLoadingScreen()}
        {this.renderGameView()}
        {this.props.gameLoaded && this.renderCompass()}
      </GameViewLayout>
    )
  }
}

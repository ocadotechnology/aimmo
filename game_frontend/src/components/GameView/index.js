import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { CircularProgress } from '@material-ui/core'
import Typography from '@material-ui/core/Typography'
import FindMeButton from 'components/FindMeButton'
import GameEngine from '../../babylon/gameEngine'
import { StandardEnvironment } from '../../babylon/environment/environment'

export const GameViewLayout = styled.div`
  grid-area: game-view;
  position: relative;
`

export const LoadingBackgroundOverlay = styled.div`
  align-items: center;
  background-color: ${props => props.theme.palette.primary.contrastText};
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  width: 100%;
`

export const OverlayElements = styled.div`
  align-items: center;
  display: flex;
  justify-content: space-between;
`

export const Overlay = styled.div`
  position: absolute;
  width: 100%;
  bottom: 0;
`

export const LoadingText = styled(Typography)`
  padding-top: ${props => props.theme.spacing(2)}px;
`

export const Compass = styled.img`
  padding-bottom: ${props => props.theme.spacing()}px;
  padding-left: ${props => props.theme.spacing()}px;
  position: sticky;
`

export const PositionedFindMeButton = styled(FindMeButton)`
  right: ${props => props.theme.spacing(3)}px;
`

export default class GameView extends Component {
  static propTypes = {
    connectToGame: PropTypes.func,
    gameLoaded: PropTypes.bool,
    cameraCenteredOnUserAvatar: PropTypes.bool,
    mapPanned: PropTypes.func,
    centerCameraOnUserAvatar: PropTypes.func,
    environment: PropTypes.object
  }

  componentDidMount () {
    if (!this.props.gameLoaded) {
      this.props.connectToGame()
    }
    const environment = this.props.environment ?? new StandardEnvironment(this.canvas)
    this.gameEngine = new GameEngine(this.handleMapPanned, environment)
  }

  componentDidUpdate (prevProps) {
    this.gameEngine.onUpdate(prevProps, this.props)
  }

  componentWillUnmount () {
    if (this.props.gameLoaded) {
      this.gameEngine.unmount()
    }
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
    return <canvas style={{ width: '100%', height: '100%' }} ref={this.onCanvasLoaded} />
  }

  renderLoadingScreen = () => {
    return (
      <LoadingBackgroundOverlay>
        <CircularProgress color='inherit' />
        <LoadingText variant='body1' color='inherit'>
          We are building your game... ⏱
        </LoadingText>
        <LoadingText variant='body1' color='inherit'>
          If the game doesn’t load after 60 seconds, please
          <a
            className="freshdesk__contact-us"
            style={{"cursor": "pointer", "textDecoration": "underline",}}
          >
            contact us.
          </a>.
        </LoadingText>
      </LoadingBackgroundOverlay>
    )
  }

  renderIcons = () => {
    return (
      <Overlay>
        <OverlayElements>
          <Compass src='/static/images/compass.svg' />
          <PositionedFindMeButton
            aria-label='Find Me'
            whenClicked={this.props.centerCameraOnUserAvatar}
            isCameraCenteredOnUserAvatar={this.props.cameraCenteredOnUserAvatar}
            id='find-me-button'
          />
        </OverlayElements>
      </Overlay>
    )
  }

  render () {
    return (
      <GameViewLayout>
        {!this.props.gameLoaded && this.renderLoadingScreen()}
        {this.renderGameView()}
        {this.props.gameLoaded && this.renderIcons()}
      </GameViewLayout>
    )
  }
}

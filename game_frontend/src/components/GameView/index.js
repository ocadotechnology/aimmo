import styled from 'styled-components'
import React, { Component } from 'react'
import Unity from 'react-unity-webgl'
import PropTypes from 'prop-types'
import Typography from '@material-ui/core/Typography'
import { CircularProgress } from '@material-ui/core'
import { unityContent } from 'api/unity'

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
  background-color: rgba(0, 0, 0, 0.2);
`

export const StyledUnity = styled(Unity)`
  display: ${props => props.gameDataLoaded ? 'block' : 'none'};
`

export const StyledCircularProgress = styled(CircularProgress)`
    max-width: 50%;
`

export const LoadingText = styled(Typography)`
  padding-top: ${props => props.theme.spacing(2)}px;
`

export default class GameView extends Component {
  constructor (props) {
    super(props)
    unityContent.on('loaded', this.unityContentLoaded)
  }

  unityContentLoaded = () => {
    this.props.connectToGame()
  }

  renderLoadingScreen = gameDataLoaded => {
    if (!gameDataLoaded) {
      return (
        <LoadingBackgroundOverlay>
          <StyledCircularProgress color='inherit' />
          <LoadingText
            variant='subtitle1'
            color='inherit'>
            Building game world...
          </LoadingText>
        </LoadingBackgroundOverlay>
      )
    }
  }

  // renderUnityView = (unityContent, gameDataLoaded) => {
  //   return (
  //     <StyledUnity
  //       gameDataLoaded={gameDataLoaded}
  //       unityContent={unityContent}
  //       height='100%'
  //       width='100%' />
  //   )
  // }

  render () {
    return (
      <GameViewLayout>
        {this.renderLoadingScreen(this.props.gameDataLoaded)}
        {/* {this.renderUnityView(unityContent, this.props.gameDataLoaded)} */}
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  connectToGame: PropTypes.func,
  gameDataLoaded: PropTypes.bool
}

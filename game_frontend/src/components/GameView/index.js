import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Environment from '../../babylon/environment'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export const StyledSVG = styled.img`
  position: ${props => props.theme.additionalVariables.compass.position};
  bottom: ${props => props.theme.additionalVariables.compass.bottom};
  left: ${props => props.theme.additionalVariables.compass.left};
  z-index: ${props => props.theme.additionalVariables.compass.zIndex};
`

export default class GameView extends Component {
  componentDidMount() {
    this.environment = new Environment(this.canvas)
    this.environment.setup()

    // Resize the babylon engine when the window is resized
    window.addEventListener('resize', this.environment.windowResized)
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
        <StyledSVG src="/static/images/compass.svg" />
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
  gameDataLoaded: PropTypes.bool
}

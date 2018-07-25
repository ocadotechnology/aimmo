import styled from 'styled-components'
import React, { Component } from 'react'
import Unity from 'react-unity-webgl'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Game'

export const GameViewLayout = styled.div`
  grid-area: game-view
`

const UNITY_LOADED = 1

export class GameView extends Component {
  onProgress (progression) {
    if (progression === UNITY_LOADED) {
      this.props.connectToGame()
    }
  }

  render () {
    return (
      <GameViewLayout>
        <Unity
          src='/static/unity/Build/unity.json'
          loader='/static/unity/Build/UnityLoader.js'
          onProgress={this.onProgress.bind(this)}
        />
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  connectToGame: PropTypes.func
}

const mapStateToProps = state => ({})

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(GameView)

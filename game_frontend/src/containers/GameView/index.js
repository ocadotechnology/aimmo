import styled from 'styled-components'
import React, { Component } from 'react'
import Unity from 'react-unity-webgl'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Game'

export const GameViewLayout = styled.div`
  grid-area: game-view
`

export class GameView extends Component {
  constructor (props) {
    super(props)

    this.props.connectToGame()
  }

  serialisedSSLFlag () {
    let boolString = this.props.gameSSL.toString()

    return boolString.charAt(0).toUpperCase() + boolString.slice(1)
  }

  render () {
    return (
      <GameViewLayout>
        <Unity
          src='/static/unity/Build/unity.json'
          loader='/static/unity/Build/UnityLoader.js'
        />
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  getConnectionParameters: PropTypes.func
}

const mapStateToProps = state => ({})

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(GameView)

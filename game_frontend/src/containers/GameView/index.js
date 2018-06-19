import styled from 'styled-components'
import React, { Component } from 'react'
import Unity, { RegisterExternalListener, UnityEvent } from 'react-unity-webgl'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Game'

const GameViewLayout = styled.div`
  grid-area: game-view
`

export class GameView extends Component {
  constructor(props) {
    super(props)

    this.props.getConnectionParams()

    RegisterExternalListener("SendAllConnect", this.sendAllConnect.bind(this))
  }

  sendAllConnect() {
    this.props.setGameURL(this.props.gameURL)
    this.props.setGamePath(this.props.gamePath)
    this.props.setGamePort(this.props.gamePort)
    this.props.setGameSSL(this.serialisedSSLFlag())
    this.props.establishGameConnection()
  }

  serialisedSSLFlag() {
    let boolString = this.props.gameSSL.toString()
    
    return boolString.charAt(0).toUpperCase() + boolString.slice(1)
  }
  
  render() {
    return (
      <GameViewLayout>
        <Unity
          src="/static/unity/Build/unity.json"
          loader="/static/unity/Build/UnityLoader.js"
        />
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  gameURL: PropTypes.string,
  gamePath: PropTypes.string,
  gamePort: PropTypes.number,
  sslFlag: PropTypes.bool,
  getConnectionParams: PropTypes.func
}

const mapStateToProps = state => ({
  gameURL: state.game.connectionParams.game_url_base,
  gamePath: state.game.connectionParams.game_url_path,
  gamePort: state.game.connectionParams.game_url_port,
  gameSSL: state.game.connectionParams.game_ssl_flag
})

const mapDispatchToProps = {
  getConnectionParams: actions.getConnectionParamsRequest,
  setGameURL: actions.setGameURL,
  setGamePath: actions.setGamePath,
  setGamePort: actions.setGamePort,
  setGameSSL: actions.setGameSSL,
  establishGameConnection: actions.establishGameConnection
}

export default connect(mapStateToProps, mapDispatchToProps)(GameView)

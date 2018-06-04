import styled from 'styled-components'
import React, { Component } from 'react'
import Unity, { RegisterExternalListener, UnityEvent } from 'react-unity-webgl'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Editor'

const GameViewLayout = styled.div`
  background-color: purple
  grid-area: game-view
`

export class GameView extends Component {
  constructor(props) {
    super(props)

    // Send a request to the Django's API to get all relevant information.
    this.props.getConnectionParams()

    RegisterExternalListener("SendAllConnect", this.sendAllConnect.bind(this))

    this.setGameURL = new UnityEvent("World Controller", "SetGameURL")
    this.setGamePort = new UnityEvent("World Controller", "SetGamePort")
    this.setGamePath = new UnityEvent("World Controller", "SetGamePath")
    this.setSSL = new UnityEvent("World Controller", "SetSSL")
    this.establishConnection = new UnityEvent("World Controller", "EstablishConnection")
  }

  sendAllConnect() {
    this.props.emitUnityEvent(this.setGameURL, this.props.gameURL)
    this.props.emitUnityEvent(this.setGamePort, this.props.gamePort)
    this.props.emitUnityEvent(this.setGamePath, this.props.gamePath)
    // TODO: convert prop bool to string here instead of hard coding
    this.props.emitUnityEvent(this.setSSL, "False")
    this.establishConnection.emit()
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
  // TODO: create issue to change this to not be inside editor reducer but instead its own one
  // EDITOR refers to the redux feature, not just the "editor" in the UI. bad naming =(
  gameURL: state.editor.connectionParams.game_url_base,
  gamePath: state.editor.connectionParams.game_url_path,
  gamePort: state.editor.connectionParams.game_url_port,
  sslFlag: state.editor.connectionParams.game_ssl_flag
})

const mapDispatchToProps = {
  getConnectionParams: actions.getConnectionParamsRequest,
  emitUnityEvent: actions.emitUnityEvent
}

export default connect(mapStateToProps, mapDispatchToProps)(GameView)

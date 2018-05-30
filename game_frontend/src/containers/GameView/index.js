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
    // It's recommended to register the callback before loading Unity.
    super(props)

    // Send a request to the Django's API to get all relevant information.
    this.props.getConnectionParams()

    RegisterExternalListener("SendAllConnect", this.sendAllConnect.bind(this))

    // TODO: probably move below to epics or something
    this.setGameURL = new UnityEvent("World Controller", "SetGameURL")
    this.setGamePort = new UnityEvent("World Controller", "SetGamePort")
    this.setGamePath = new UnityEvent("World Controller", "SetGamePath")
    this.setSSL = new UnityEvent("World Controller", "SetSSL")
    this.establishConnection = new UnityEvent("World Controller", "EstablishConnection")
  }

  sendAllConnect() {
    // TODO: do some checking if canEmit before actually doing it (FIRST DO THIS IN EPICS)
    console.log("sendAllConnect hit")
    this.setGameURL.emit(this.props.gameURL)
    this.setGamePort.emit(this.props.gamePort)
    this.setGamePath.emit(this.props.gamePath)
    // TODO: convert prop bool to string here instead of hard coding
    this.setSSL.emit("False")
    this.establishConnection.emit()
    console.log("finished")
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
  // TODO: change this to not be inside editor reducer but instead its own one
  gameURL: state.editor.connectionParams.game_url_base,
  gamePath: state.editor.connectionParams.game_url_path,
  gamePort: state.editor.connectionParams.game_url_port,
  sslFlag: state.editor.connectionParams.game_ssl_flag
})

const mapDispatchToProps = {
  getConnectionParams: actions.getConnectionParamsRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(GameView)

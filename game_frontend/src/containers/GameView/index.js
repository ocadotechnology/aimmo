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
  }

  sendAllConnect() {
    this.props.emitUnityEvent("World Controller", "SetGameURL", this.props.gameURL)
    this.props.emitUnityEvent("World Controller", "SetGamePort", this.props.gamePort)
    this.props.emitUnityEvent("World Controller", "SetGamePath", this.props.gamePath)
    this.props.emitUnityEvent("World Controller", "SetSSL", this.serialisedSSLFlag())
    this.props.emitUnityEvent("World Controller", "EstablishConnection", undefined)
  }

  serialisedSSLFlag() {
    // Converts the prop bool value "sslFlag" to a string and capitalises
    // the first letter to be ready to be used on Unity's side.
    let boolString = this.props.sslFlag.toString()
    
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

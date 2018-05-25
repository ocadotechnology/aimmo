import styled from 'styled-components'
import React, { Component } from 'react'
import Unity, { RegisterExternalListener, UnityEvent } from "react-unity-webgl"
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

const GameViewLayout = styled.div`
  background-color: purple
  grid-area: game-view
`

export class GameView extends Component {
  constructor() {
    // It's recommended to register the callback before loading Unity.
    super()
    console.log("constructor")
    RegisterExternalListener("SendAllConnect", this.sendAllConnect.bind(this))
    // TODO: probably move below to epics or something
    this.setGameURL = new UnityEvent("World Controller", "SetGameURL")
    this.setGamePort = new UnityEvent("World Controller", "SetGamePort")
    this.setGamePath = new UnityEvent("World Controller", "SetGamePath")
    this.setSSL = new UnityEvent("World Controller", "SetSSL")
    this.establishConnection = new UnityEvent("World Controller", "EstablishConnection")
  }

  sendAllConnect() {
    console.log("sendAllConnect hit")
    this.setGameURL("test")
    this.setGamePort(0)
    this.setGamePath("/yo")
    this.setSSL("True")
    this.establishConnection()
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

const mapStateToProps = () => ({})

const mapDispatchToProps = {}

export default connect(mapStateToProps, mapDispatchToProps)(GameView)

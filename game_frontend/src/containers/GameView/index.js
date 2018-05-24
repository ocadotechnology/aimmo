import styled from 'styled-components'
import React, { Component } from 'react'
import Unity, { RegisterExternalListener } from "react-unity-webgl"
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
    RegisterExternalListener("SendAllConnect", this.sendAllConnect.bind(this))
  }

  sendAllConnect() {
    console.log("sendAllConnect hit")
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
export default connect(mapStateToProps, mapDispatchToProps)(GameView)

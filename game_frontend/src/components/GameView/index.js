import styled from 'styled-components'
import React, { Component } from 'react'
import Unity from 'react-unity-webgl'
import PropTypes from 'prop-types'
import { LinearProgress } from '@material-ui/core'
import { unityContent } from 'api/unity'

export const GameViewLayout = styled.div`
  grid-area: game-view;
`

export default class GameView extends Component {
  state = {
    unityContentLoaded: false
  }

  constructor (props) {
    super(props)
    this.state = {
      unityContent
    }
    unityContent.on('loaded', this.unityContentLoaded)
  }

  unityContentLoaded = () => {
    this.setState({
      unityContentLoaded: true
    })
    this.props.connectToGame()
  }

  renderloadingBar = unityContentLoaded => {
    if (!unityContentLoaded) {
      return (
        <LinearProgress color='secondary' />
      )
    }
  }

  renderUnityView = unityContent => {
    return (
      <Unity
        unityContent={unityContent}
        height='100%'
        width='100%' />
    )
  }

  render () {
    return (
      <GameViewLayout>
        {this.renderloadingBar(this.state.unityContentLoaded)}
        {this.renderUnityView(this.state.unityContent)}
      </GameViewLayout>
    )
  }
}

GameView.propTypes = {
  connectToGame: PropTypes.func
}

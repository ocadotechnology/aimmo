import React, { Component, Fragment } from 'react'
import GameMenu from 'components/GameMenu'
import GameView from 'containers/GameView'

export default class Game extends Component {
  render () {
    return (
      <Fragment>
        <GameMenu />
        <GameView />
      </Fragment>
    )
  }
}

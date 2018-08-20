import React, { Component, Fragment } from 'react'
import GameMenu from 'components/GameMenu'
import GameView from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/Game'

export class Game extends Component {
  render () {
    return (
      <Fragment>
        <GameMenu />
        <GameView connectToGame={this.props.connectToGame} />
      </Fragment>
    )
  }
}

Game.propTypes = {
  connectToGame: PropTypes.func
}

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest
}

export default connect(null, mapDispatchToProps)(Game)

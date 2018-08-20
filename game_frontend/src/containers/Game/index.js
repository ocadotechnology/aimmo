import React, { Component, Fragment } from 'react'
import GameMenu from 'components/GameMenu'
import { GameView } from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/GhibliMovies'

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

const mapStateToProps = state => ({})

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(Game)

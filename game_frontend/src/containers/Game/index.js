import React, { Component, Fragment } from 'react'
import GameView from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/Game'
import Snackbar, { SnackbarTypes } from 'components/Snackbar'

export class Game extends Component {
  static propTypes = {
    connectToGame: PropTypes.func,
    theme: PropTypes.object,
    showSnackbar: PropTypes.bool,
    snackbarMessage: PropTypes.string,
    snackbarType: PropTypes.oneOf(Object.values(SnackbarTypes))
  }

  state = {
    showSnackbar: this.props.showSnackbar
  }

  componentWillReceiveProps (nextProps) {
    if (nextProps.showSnackbar !== this.props.showSnackbar) {
      this.setState({
        showSnackbar: nextProps.showSnackbar
      })
    }
  }

  handleClose = () => {
    this.setState({ showSnackbar: false })
    this.props.snackbarShown()
  }

  render () {
    return (
      <Fragment>
        <GameView
          connectToGame={this.props.connectToGame}
          gameState={this.props.gameState}
          currentAvatarID={this.props.currentAvatarID}
        />
        <Snackbar
          type='success'
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          open={this.state.showSnackbar}
          direction='up'
          onClose={this.handleClose}
          message={this.props.snackbarMessage}
        />
      </Fragment>
    )
  }
}

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest,
  snackbarShown: actions.snackbarShown
}

const mapStateToProps = state => ({
  showSnackbar: state.game.showSnackbar,
  snackbarMessage: state.game.snackbarMessage,
  gameState: state.game.gameState,
  currentAvatarID: state.game.connectionParameters.currentAvatarID
})

export default connect(mapStateToProps, mapDispatchToProps)(Game)

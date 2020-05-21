import React, { Component } from 'react'
import GameView from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/Game'
import Snackbar from 'components/Snackbar'

export class Game extends Component {
  static propTypes = {
    connectToGame: PropTypes.func,
    showSnackbar: PropTypes.bool,
    snackbarMessage: PropTypes.string,
    snackbarShown: PropTypes.func,
    gameState: PropTypes.object,
    currentAvatarID: PropTypes.number,
    gameLoaded: PropTypes.bool,
    centerCameraOnUserAvatar: PropTypes.func,
    cameraCenteredOnUserAvatar: PropTypes.bool,
    mapPanned: PropTypes.func
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
      <>
        <GameView
          connectToGame={this.props.connectToGame}
          gameState={this.props.gameState}
          currentAvatarID={this.props.currentAvatarID}
          gameLoaded={this.props.gameLoaded}
          cameraCenteredOnUserAvatar={this.props.cameraCenteredOnUserAvatar}
          mapPanned={this.props.mapPanned}
          centerCameraOnUserAvatar={this.props.centerCameraOnUserAvatar}
        />
        <Snackbar
          type='success'
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          open={this.state.showSnackbar}
          direction='up'
          onClose={this.handleClose}
          message={this.props.snackbarMessage}
        />
      </>
    )
  }
}

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest,
  snackbarShown: actions.snackbarShown,
  mapPanned: actions.mapPanned,
  centerCameraOnUserAvatar: actions.centerCameraOnUserAvatar
}

const mapStateToProps = state => ({
  showSnackbar: state.game.showSnackbar,
  snackbarMessage: state.game.snackbarMessage,
  gameState: state.game.gameState,
  currentAvatarID: state.game.connectionParameters.currentAvatarID,
  gameLoaded: state.game.gameLoaded,
  cameraCenteredOnUserAvatar: state.game.cameraCenteredOnUserAvatar
})

export default connect(mapStateToProps, mapDispatchToProps)(Game)

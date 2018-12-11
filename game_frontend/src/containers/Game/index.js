import React, { Component, Fragment } from 'react'
import GameView from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/Game'
import Snackbar from 'components/Snackbar'

export class Game extends Component {
  static propTypes = {
    connectToGame: PropTypes.func,
    theme: PropTypes.object
  }

  state = {
    showSnackbar: this.props.showSnackbarForAvatarUpdated
  }

  componentWillReceiveProps (nextProps) {
    if (nextProps.showSnackbarForAvatarUpdated !== this.props.showSnackbarForAvatarUpdated) {
      this.setState({
        showSnackbar: nextProps.showSnackbarForAvatarUpdated
      })
    }
  }

  handleClose = () => {
    this.setState({ showSnackbar: false })
    this.props.snackbarForAvatarUpdatedShown()
  }

  render () {
    return (
      <Fragment>
        <GameView
          connectToGame={this.props.connectToGame}
          gameDataLoaded={this.props.gameDataLoaded}
        />
        <Snackbar
          type='success'
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          open={this.state.showSnackbar}
          direction='up'
          onClose={this.handleClose}
          message='Your Avatar has been updated with your new code!'
        />
      </Fragment>
    )
  }
}

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest,
  snackbarForAvatarUpdatedShown: actions.snackbarForAvatarUpdatedShown
}

const mapStateToProps = state => ({
  showSnackbarForAvatarUpdated: state.game.showSnackbarForAvatarUpdated,
  gameDataLoaded: state.game.gameDataLoaded
})

export default connect(mapStateToProps, mapDispatchToProps)(Game)

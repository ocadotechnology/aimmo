import React, { Component, Fragment } from 'react'
import GameView from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/Game'
import Snackbar from 'components/Snackbar'
import { withTheme } from '@material-ui/core/styles'

export class Game extends Component {
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

  static propTypes = {
    connectToGame: PropTypes.func,
    theme: PropTypes.object
  }

  render () {
    const { theme } = this.props
    return (
      <Fragment>
        <GameView connectToGame={this.props.connectToGame} />
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          open={this.state.showSnackbar}
          direction='up'
          autoHideDuration={theme.transitions.duration.enteringScreen + 2000 + theme.transitions.duration.leavingScreen}
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
  showSnackbarForAvatarUpdated: state.game.showSnackbarForAvatarUpdated
})

export default connect(mapStateToProps, mapDispatchToProps)(withTheme()(Game))

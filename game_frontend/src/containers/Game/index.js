import React, { Component } from 'react'
import GameView from 'components/GameView'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'redux/features/Game'

export class Game extends Component {
  static propTypes = {
    connectToGame: PropTypes.func,
    gameState: PropTypes.object,
    currentAvatarID: PropTypes.number,
    gameLoaded: PropTypes.bool,
    centerCameraOnUserAvatar: PropTypes.func,
    cameraCenteredOnUserAvatar: PropTypes.bool,
    mapPanned: PropTypes.func,
  }

  render() {
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
      </>
    )
  }
}

const mapDispatchToProps = {
  connectToGame: actions.socketConnectToGameRequest,
  mapPanned: actions.mapPanned,
  centerCameraOnUserAvatar: actions.centerCameraOnUserAvatar,
}

const mapStateToProps = (state) => ({
  gameState: state.game.gameState,
  currentAvatarID: state.game.connectionParameters.currentAvatarID,
  gameLoaded: state.game.gameLoaded,
  cameraCenteredOnUserAvatar: state.game.cameraCenteredOnUserAvatar,
})

export default connect(mapStateToProps, mapDispatchToProps)(Game)

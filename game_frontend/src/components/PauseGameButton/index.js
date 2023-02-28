import { Button } from '@material-ui/core'
import React, { Component } from 'react'

export default class PauseGameButton extends Component {
  static propTypes = {
    gamePaused: PropTypes.bool,
  }

  render() {
    return <Button>{true ? 'Pause Game' : 'Resume game'}</Button>
  }
}

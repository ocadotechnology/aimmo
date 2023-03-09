import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Fab from '@material-ui/core/Fab'
import PlayIcon from 'components/icons/Play'
import BugIcon from 'components/icons/Bug'
import { CircularProgress } from '@material-ui/core'
import CheckCircle from 'components/icons/CheckCircle'

export const MarginedPlayIcon = styled(PlayIcon)`
  margin-right: ${(props) => props.theme.spacing()}px;
`

export const MarginedCircularProgress = styled(CircularProgress)`
  margin-right: ${(props) => props.theme.spacing()}px;
`

export const MarginedCheckCircle = styled(CheckCircle)`
  margin-right: ${(props) => props.theme.spacing()}px;
`

export const MarginedBugIcon = styled(BugIcon)`
  margin-right: ${(props) => props.theme.spacing()}px;
`

export const RunCodeButtonStatus = Object.freeze({
  normal: 'normal',
  updating: 'updating',
  error: 'error',
  done: 'done',
})

export default class RunCodeButton extends Component {
  static propTypes = {
    whenClicked: PropTypes.func,
    runCodeButtonStatus: PropTypes.shape({
      status: PropTypes.oneOf([
        RunCodeButtonStatus.normal,
        RunCodeButtonStatus.updating,
        RunCodeButtonStatus.error,
        RunCodeButtonStatus.done,
      ]),
    }),
    isCodeOnServerDifferent: PropTypes.bool,
    className: PropTypes.string,
  }

  shouldButtonBeDisabled = () => {
    switch (this.props.runCodeButtonStatus.status) {
      case RunCodeButtonStatus.error:
      case RunCodeButtonStatus.done:
        return false
      default:
        return (
          !this.props.isCodeOnServerDifferent ||
          this.props.runCodeButtonStatus.status === RunCodeButtonStatus.updating
        )
    }
  }

  shouldButtonBeClickable() {
    return (
      !this.shouldButtonBeDisabled() ||
      this.props.runCodeButtonStatus.status !== RunCodeButtonStatus.done ||
      this.props.runCodeButtonStatus.status !== RunCodeButtonStatus.error
    )
  }

  renderContent(status) {
    switch (status) {
      case RunCodeButtonStatus.normal:
        return (
          <>
            <MarginedPlayIcon />
            Run code
          </>
        )
      case RunCodeButtonStatus.updating:
        return (
          <>
            <MarginedCircularProgress color="inherit" size="24px" />
            Updating
          </>
        )
      case RunCodeButtonStatus.error:
        return (
          <>
            <MarginedBugIcon />
            Error!
          </>
        )
      case RunCodeButtonStatus.done:
        return (
          <>
            <MarginedCheckCircle />
            Done
          </>
        )
    }
  }

  render() {
    return (
      <Fab
        color="primary"
        className={this.props.className}
        disabled={this.shouldButtonBeDisabled()}
        aria-label="Run Code"
        variant="extended"
        id="post-code-button"
        onClick={this.shouldButtonBeClickable() ? this.props.whenClicked : () => {}}
      >
        {this.renderContent(this.props.runCodeButtonStatus.status)}
      </Fab>
    )
  }
}

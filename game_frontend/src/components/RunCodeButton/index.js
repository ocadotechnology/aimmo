import styled from 'styled-components'
import React, { Component } from 'react'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import Button from '@material-ui/core/Button'
import PlayIcon from 'components/icons/Play'
import BugIcon from 'components/icons/Bug'
import { CircularProgress } from '@material-ui/core'
import CheckCircle from 'components/icons/CheckCircle'

export const MarginedPlayIcon = styled(PlayIcon)`
  margin-right: ${props => props.theme.spacing.unit}px;
`

export const MarginedCircularProgress = styled(CircularProgress)`
  margin-right: ${props => props.theme.spacing.unit}px;
`

export const MarginedCheckCircle = styled(CheckCircle)`
  margin-right: ${props => props.theme.spacing.unit}px;
`

export const MarginedBugIcon = styled(BugIcon)`
  margin-right: ${props => props.theme.spacing.unit}px;
`

export const RunCodeButtonStatus = Object.freeze({
  normal: 'normal',
  updating: 'updating',
  done: 'done'
})

export class RunCodeButton extends Component {
  shouldButtonBeDisabled () {
    if (this.props.timeoutStatus) {
      return false
    } else {
      if (this.props.runCodeButtonStatus.status === RunCodeButtonStatus.done) {
        return false
      }
      return !this.props.isCodeOnServerDifferent ||
        this.props.runCodeButtonStatus.status === RunCodeButtonStatus.updating
    }
  }

  shouldButtonBeClickable () {
    return (!(this.shouldButtonBeDisabled() && this.props.runCodeButtonStatus === RunCodeButtonStatus.done) ||
            !this.props.timeoutStatus)
  }

  renderContent (status) {
    if (this.props.timeoutStatus) {
      return (
        <>
          <MarginedBugIcon />Error
        </>
      )
    } else {
      switch (status) {
        case RunCodeButtonStatus.normal:
          return (
          <>
            <MarginedPlayIcon />Run Code
          </>
          )
        case RunCodeButtonStatus.updating:
          return (
          <>
            <MarginedCircularProgress
              color='inherit'
              size='24px' />Updating
          </>
          )
        case RunCodeButtonStatus.done:
          return (
            <>
              <MarginedCheckCircle />Done
          </>
          )
      }
    }
  }

  render () {
    return (
      <Button
        color='secondary'
        className={this.props.className}
        disabled={this.shouldButtonBeDisabled()}
        aria-label='Run Code'
        variant='extendedFab'
        id='post-code-button'
        onClick={this.shouldButtonBeClickable() ? () => { } : this.props.whenClicked}>
        {this.renderContent(this.props.runCodeButtonStatus.status)}
      </Button>
    )
  }
}

RunCodeButton.propTypes = {
  whenClicked: PropTypes.func,
  runCodeButtonStatus: PropTypes.shape({
    status: PropTypes.oneOf([
      RunCodeButtonStatus.normal,
      RunCodeButtonStatus.updating,
      RunCodeButtonStatus.done]
    )
  }),
  isCodeOnServerDifferent: PropTypes.bool,
  className: PropTypes.string
}

const mapStateToProps = state => ({
  timeoutStatus: state.game.timeoutStatus
})

export default connect(mapStateToProps)(RunCodeButton)

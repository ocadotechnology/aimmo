import React, { Component } from 'react'
import styled from 'styled-components'
import PropTypes from 'prop-types'
import { withTheme } from '@material-ui/core/styles'

import MaterialSnackbar from '@material-ui/core/Snackbar'
import MaterialSnackbarContent from '@material-ui/core/SnackbarContent'

import CheckCircleIcon from 'components/icons/CheckCircle'
import BugIcon from 'components/icons/Bug'
import WarningIcon from '@material-ui/icons/Warning'
import InfoIcon from '@material-ui/icons/Info'

export const SnackbarContentLayout = styled.span`
  display: flex;
  align-items: center;
`

export const StyledSnackbarContent = styled(MaterialSnackbarContent)`
  && {
    border-radius: ${props => props.theme.additionalVariables.snackbar.borderRadius};
  }
`
export const SnackbarTypes = Object.freeze({
  success: 'success',
  warning: 'warning',
  error: 'error',
  info: 'info'
})

export class Snackbar extends Component {
  static duration = 4000
  static muiName = 'Snackbar'

  static propTypes = {
    type: PropTypes.oneOf(Object.values(SnackbarTypes)).isRequired,
    message: PropTypes.string.isRequired,
    open: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    anchorOrigin: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired
  }

  static iconVariants = {
    success: CheckCircleIcon,
    warning: WarningIcon,
    error: BugIcon,
    info: InfoIcon
  }

  getStyledIcon = () => {
    const { type } = this.props
    const Icon = Snackbar.iconVariants[type]
    return styled(Icon)`
      margin-right: ${props => props.theme.spacing()}px;
    `
  }

  durationIncludingTransitionTime = () => {
    const { theme } = this.props
    return (
      theme.transitions.duration.enteringScreen +
      Snackbar.duration +
      theme.transitions.duration.leavingScreen
    )
  }

  render () {
    const { message } = this.props
    const StyledIcon = this.getStyledIcon()
    return (
      <MaterialSnackbar {...this.props} autoHideDuration={this.durationIncludingTransitionTime()}>
        <StyledSnackbarContent
          message={
            <SnackbarContentLayout>
              <StyledIcon />
              {message}
            </SnackbarContentLayout>
          }
        />
      </MaterialSnackbar>
    )
  }
}

export default withTheme(Snackbar)

import styled from 'styled-components'
import PropTypes from 'prop-types'
import React, { Component } from 'react'
import { Fab } from '@material-ui/core'
import FindMeIcon from 'components/icons/FindMe'

export const MarginedLocationIcon = styled(FindMeIcon)`
  margin-right: ${(props) => props.theme.spacing()}px;
`

export default class FindMeButton extends Component {
  static propTypes = {
    whenClicked: PropTypes.func,
    isCameraCenteredOnUserAvatar: PropTypes.bool,
    className: PropTypes.string,
  }

  render() {
    return (
      <Fab
        color="primary"
        className={this.props.className}
        disabled={this.props.isCameraCenteredOnUserAvatar}
        aria-label="Find Me"
        id="find-me-button"
        variant="extended"
        onClick={this.props.whenClicked}
      >
        <MarginedLocationIcon color="inherit" />
        Find me
      </Fab>
    )
  }
}

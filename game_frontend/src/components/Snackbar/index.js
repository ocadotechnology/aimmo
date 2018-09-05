import React, { Component } from 'react'
import MaterialSnackbar from '@material-ui/core/Snackbar'
import PropTypes from 'prop-types'

export default class Snackbar extends Component {
  render () {
    return (
      <MaterialSnackbar {...this.props} />
    )
  }
}

Snackbar.proptypes = PropTypes.object

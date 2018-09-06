import React, { Component } from 'react'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'
import theme from 'theme'
import PropTypes from 'prop-types'

export default class ThemeProvider extends Component {
  static propTypes = {
    variant: PropTypes.oneOf(['light', 'dark']).isRequired
  }

  createTheme = type => {
    const palette = { ...theme.palette, type }
    return createMuiTheme({ ...theme, palette })
  }

  render () {
    const muiTheme = this.createTheme(this.props.variant)
    return (
      <StyledComponentsThemeProvider theme={muiTheme}>
        <MuiThemeProvider theme={muiTheme} >
          {this.props.children}
        </MuiThemeProvider>
      </StyledComponentsThemeProvider>
    )
  }
}

import React, { Component } from 'react'
import styled from 'styled-components'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import IconButton from '@material-ui/core/IconButton'
import CloseIcon from 'components/icons/Close'

export const NavigationBarLayout = styled.nav`
    grid-area: navigation-bar;
`

export const CloseToolbar = styled(Toolbar)`
  justify-content: flex-end;
`

export default class NavigationBar extends Component {
  render () {
    return (
      <NavigationBarLayout>
        <AppBar
          position='sticky'>
          <CloseToolbar>
            <IconButton
              href='/aimmo'
              aria-label='Close'
              color='inherit'>
              <CloseIcon />
            </IconButton>
          </CloseToolbar>
        </AppBar>
      </NavigationBarLayout>
    )
  }
}

import React, { Component } from 'react'
import styled from 'styled-components'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import IconButton from '@material-ui/core/IconButton'
import CloseIcon from 'components/icons/Close'

export const NavigationBarLayout = styled.nav`
    grid-area: navigation-bar;
`

export const RightToolbar = styled(Toolbar)`
  justify-content: flex-end;
`

export default class NavigationBar extends Component {
  render () {
    return (
      <NavigationBarLayout>
        <AppBar
          color='secondary'
          position='sticky'>
          <RightToolbar>
            <IconButton
              href='/aimmo'
              aria-label='Close'
              color='inherit'>
              <CloseIcon />
            </IconButton>
          </RightToolbar>
        </AppBar>
      </NavigationBarLayout>
    )
  }
}

import React, { Component } from 'react'
import styled from 'styled-components'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import IconButton from '@material-ui/core/IconButton'

export const NavigationBarLayout = styled.nav`
    grid-area: navigation-bar;
`

export const HomeToolbar = styled(Toolbar)`
  justify-content: flex-start;
`

export default class NavigationBar extends Component {
  render () {
    return (
      <NavigationBarLayout>
        <AppBar
          position='sticky'>
          <HomeToolbar>
            <IconButton
              href='/kurono'
              aria-label='Home'
              color='inherit'>
              <img src='/static/images/kurono_logo_mark.svg' height='50px' alt='Kurono Logo' />
            </IconButton>
          </HomeToolbar>
        </AppBar>
      </NavigationBarLayout>
    )
  }
}

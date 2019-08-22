import React, { Component } from 'react'
import styled from 'styled-components'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import IconButton from '@material-ui/core/IconButton'
import KuronoLogo from 'components/icons/KuronoLogo'

export const NavigationBarLayout = styled.nav`
    grid-area: navigation-bar;
`
export const LogoToolbar = styled(Toolbar)`
  justify-content: flex-start;
`

export default class NavigationBar extends Component {
  render () {
    return (
      <NavigationBarLayout>
        <AppBar
          position='sticky'>
          <LogoToolbar>
            <IconButton
              href='/kurono'
              aria-label='Kurono dashboard'
              color='inherit'>
              <KuronoLogo fontSize='large' />
            </IconButton>
          </LogoToolbar>
        </AppBar>
      </NavigationBarLayout>
    )
  }
}

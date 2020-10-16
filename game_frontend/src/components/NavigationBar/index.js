import React, { Component } from 'react'
import styled from 'styled-components'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import { IconButton, Button } from '@material-ui/core'
import KuronoLogo from 'components/icons/KuronoLogo'

export const NavigationBarLayout = styled.nav`
    grid-area: navigation-bar;
`
export const LogoToolbar = styled(Toolbar)`
  justify-content: flex-start;
`

export const KuronoAppBar = styled(AppBar)`
  flex-direction: row;
  justify-content: space-between;
`

const appData = window.appData;
const urlForAimmoDashboard = (appData && appData.urlForAimmoDashboard) ? appData.urlForAimmoDashboard : '';

export default class NavigationBar extends Component {
  render () {
    return (
      <NavigationBarLayout>
        <KuronoAppBar
          color='secondary'
          position='sticky'
        >
          <LogoToolbar>
            <IconButton
              href={urlForAimmoDashboard}
              aria-label='Kurono dashboard'
              color='inherit'
            >
              <KuronoLogo fontSize='large' />
            </IconButton>
          </LogoToolbar>
          <Toolbar>
            <Button
              href={urlForAimmoDashboard}
              variant='outlined'
            >
              Exit game
            </Button>
          </Toolbar>
        </KuronoAppBar>
      </NavigationBarLayout>
    )
  }
}

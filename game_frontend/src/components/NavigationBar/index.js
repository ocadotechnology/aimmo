import React, { Component } from 'react'
import styled from 'styled-components'

import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import { IconButton, Button } from '@material-ui/core'

import KuronoLogo from 'components/icons/KuronoLogo'
import BadgeModal, { getBadges } from 'components/Badge'

export const NavigationBarLayout = styled.nav`
  grid-area: navigation-bar;
`
export const LogoToolbar = styled(Toolbar)`
  justify-content: flex-start;
  height: 90px;
`

export const KuronoLogoStyled = styled(KuronoLogo)`
  font-size: 3.5rem;
`

export const KuronoAppBar = styled(AppBar)`
  flex-direction: row;
  justify-content: space-between;
`

const appData = window.appData
const urlForAimmoDashboard =
  appData && appData.urlForAimmoDashboard ? appData.urlForAimmoDashboard : ''

const BADGE_MODAL_TIME = 5000

export default class NavigationBar extends Component {
  state = { modalOpen: false, completedTask: 0 }

  handleOpen = () => {
    this.setState(
      {
        modalOpen: true,
        completedTask: 1,
      },
      () => {
        setTimeout(this.handleClose, BADGE_MODAL_TIME)
      }
    )
  }

  handleClose = () => {
    this.setState({
      modalOpen: false,
    })
  }

  getFinishedTasks = () => {
    return [0, 1, 2]
  }

  renderLogoToolbar = () => {
    const finishedTasks = this.getFinishedTasks()
    const badges = getBadges(finishedTasks)
    return (
      <LogoToolbar>
        <IconButton href={urlForAimmoDashboard} aria-label="Kurono dashboard" color="inherit">
          <KuronoLogoStyled />
        </IconButton>
        {badges}
        <Button onClick={this.handleOpen}>Open modal</Button>
      </LogoToolbar>
    )
  }

  renderButtonToolbar = () => {
    return (
      <Toolbar>
        <Button href={urlForAimmoDashboard} variant="outlined">
          Exit game
        </Button>
      </Toolbar>
    )
  }

  render() {
    return (
      <NavigationBarLayout>
        <KuronoAppBar color="secondary" position="sticky">
          {this.renderLogoToolbar()}
          {this.renderButtonToolbar()}
        </KuronoAppBar>
        <BadgeModal taskId={this.state.completedTask} modalOpen={this.state.modalOpen} />
      </NavigationBarLayout>
    )
  }
}

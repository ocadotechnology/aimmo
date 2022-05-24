import React, { Component } from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'

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

class NavigationBar extends Component {
  state = { modalOpen: false, completedTasks: [], lastTask: '' }

  handleClose = () => {
    this.setState({
      modalOpen: false,
    })
  }

  static getDerivedStateFromProps(props, state) {
    // Any time completedTasks change, pass the new info as state
    if (props.completedTasks !== undefined) {
      // convert to string for comparison
      const stateTasksString = state.completedTasks.join() + ','

      if (props.completedTasks !== stateTasksString) {
        let newTasks = props.completedTasks.split(',')
        newTasks = newTasks.filter((s) => s) // remove empty element
        const lastTask = newTasks[newTasks.length - 1] // assume the last element is the last task

        return {
          modalOpen: props.modalOpen,
          completedTasks: newTasks,
          lastTask: lastTask,
        }
      }
    }
    return null // no change
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true }
  }

  renderLogoToolbar = () => {
    const badges = getBadges(this.state.completedTasks)
    return (
      <LogoToolbar>
        <IconButton href={urlForAimmoDashboard} aria-label="Kurono dashboard" color="inherit">
          <KuronoLogoStyled />
        </IconButton>
        {badges}
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
    if (this.state.modalOpen) {
      setTimeout(this.handleClose, BADGE_MODAL_TIME)
    }

    return (
      <NavigationBarLayout>
        <KuronoAppBar color="secondary" position="sticky">
          {this.renderLogoToolbar()}
          {this.renderButtonToolbar()}
        </KuronoAppBar>
        <BadgeModal taskId={this.state.lastTask} modalOpen={this.state.modalOpen} />
      </NavigationBarLayout>
    )
  }
}

const mapStateToProps = (state) => ({
  completedTasks: state.avatarWorker.completedTasks,
  modalOpen: state.avatarWorker.modalOpen,
})

export default connect(mapStateToProps)(NavigationBar)

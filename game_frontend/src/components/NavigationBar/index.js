import React, { Component } from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'

import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import { IconButton, Button } from '@material-ui/core'

import KuronoLogo from 'components/icons/KuronoLogo'
import BadgeModal, { getBadges } from 'components/Badge'
import { avatarWorkerActions } from 'features/AvatarWorker'

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

export class NavigationBar extends Component {
  static propTypes = {
    // the props received from redux state or reducers
    modalOpen: PropTypes.bool,
    completedBadges: PropTypes.string,
    badgesInit: PropTypes.func,
    gameState: PropTypes.any,
  }

  state = { modalOpen: false, completedBadges: [], lastBadge: '' }

  componentDidMount() {
    this.props.badgesInit()
  }

  handleClose = () => {
    this.setState({
      modalOpen: false,
    })
  }

  static getDerivedStateFromProps(props, state) {
    // Any time completedTasks change, pass the new info as state
    if (props.completedBadges !== undefined && props.gameState !== undefined) {
      const worksheetID = props.gameState.worksheetID
      let badges = props.completedBadges.split(',')
      badges = badges.filter((s) => s) // remove empty element
      // remove any badge that's not relevant to the current worksheet
      badges = badges.filter((b) => {
        return b.startsWith(worksheetID + ':')
      })

      // convert to string for comparison
      const stateBadgesString = state.completedBadges.join() + ','

      if (props.completedBadges !== stateBadgesString) {
        const lastBadge = badges[badges.length - 1] // assume the last element is the last badge
        // return badge info with popup if there is a new badge earned
        return {
          modalOpen: props.modalOpen,
          completedBadges: badges,
          lastBadge: lastBadge,
        }
      }
    }
    return null // no change
  }

  renderLogoToolbar = () => {
    const badges = getBadges(this.state.completedBadges)
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
    // when modalOpen changes to true, start the timer
    if (this.state.modalOpen) {
      setTimeout(this.handleClose, BADGE_MODAL_TIME)
    }

    return (
      <NavigationBarLayout>
        <KuronoAppBar color="secondary" position="sticky">
          {this.renderLogoToolbar()}
          {this.renderButtonToolbar()}
        </KuronoAppBar>
        <BadgeModal badgeId={this.state.lastBadge} modalOpen={this.state.modalOpen} />
      </NavigationBarLayout>
    )
  }
}

const mapStateToProps = (state) => ({
  completedBadges: state.avatarWorker.completedBadges,
  modalOpen: state.avatarWorker.modalOpen,
  gameState: state.game.gameState,
})

const mapDispatchToProps = {
  badgesInit: avatarWorkerActions.getBadgesRequest,
}

export default connect(mapStateToProps, mapDispatchToProps)(NavigationBar)

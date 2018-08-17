import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Button from '@material-ui/core/Button'
import { CloseIcon } from '../icons'

const GameMenuLayout = styled.nav`
  background-color: ${props => props.theme.palette.background.default}
  grid-area: game-menu
`

export default class GameMenu extends Component {
  render () {
    return (
      <GameMenuLayout>
        <Button
          id='close-game-button'> <CloseIcon /> </Button>
      </GameMenuLayout>
    )
  }
}

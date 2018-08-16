import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Editor'

export const IDEMenuLayout = styled.nav`
  background-color: ${props => props.theme.palette.background.default};
  grid-area: ide-menu;
`

export default class IDEMenu extends Component {
  render () {
    return (
      <IDEMenuLayout>
      </IDEMenuLayout>
    )
  }
}

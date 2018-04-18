import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

const IDEMenuLayout = styled.nav`
  background-color: pink
  grid-area: ide-menu
`

export default class IDEMenu extends Component {
  render () {
    return (
      <IDEMenuLayout>
        <button onClick={this.props.getCode} >Get Code</button>
      </IDEMenuLayout>
    )
  }
}

IDEMenu.propTypes = {
  getCode: PropTypes.func
}

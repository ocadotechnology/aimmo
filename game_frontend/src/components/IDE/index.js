import styled from 'styled-components'
import React, { Component, Fragment } from 'react'

export const IDEMenu = styled.nav`
  background-color: pink
  grid-area: ide-menu
`

export const IDEEditor = styled.div`
  background-color: #2F4F4F
  grid-area: ide-editor
`

export const IDEConsole = styled.div`
  background-color: #DDDDDD
  grid-area: ide-console
`

export default class IDE extends Component {
  render () {
    return (
      <Fragment>
        <IDEMenu />
        <IDEEditor />
        <IDEConsole />
      </Fragment>
    )
  }
}

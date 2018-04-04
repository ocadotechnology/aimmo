import React, { Component, Fragment } from 'react'
import IDEMenu from 'components/IDEMenu'
import IDEEditor from 'components/IDEEditor'
import IDEConsole from 'components/IDEConsole'

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

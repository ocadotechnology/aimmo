import React, { Component, Fragment } from 'react'
import IDEMenu from 'containers/IDEMenu'
import IDEEditor from 'containers/IDEEditor'
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

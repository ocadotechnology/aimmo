import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import IDEMenu from 'components/IDEMenu'
import IDEEditor from 'components/IDEEditor'
import IDEConsole from 'components/IDEConsole'

export default class IDE extends Component {
  render () {
    return (
      <Fragment>
        <IDEMenu getCode={this.props.getCode} postCode={this.props.postCode} />
        <IDEEditor code={this.props.code} />
        <IDEConsole />
      </Fragment>
    )
  }
}

IDE.propTypes = {
  code: PropTypes.string,
  getCode: PropTypes.func,
  postCode: PropTypes.func
}

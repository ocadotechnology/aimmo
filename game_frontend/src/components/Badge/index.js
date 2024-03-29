import React, { Component } from 'react'
import styled from 'styled-components'
import PropTypes from 'prop-types'

import Box from '@material-ui/core/Box'
import Modal from '@material-ui/core/Modal'
import Typography from '@material-ui/core/Typography'

import { badgeInfo } from './badges'

const BadgeModalBox = styled(Box)`
  position: absolute;
  top: 15%;
  left: 65%;
  width: 400px;
  background-color: #fff;
  border-radius: 10px;
  padding: 25px;
  opacity: 0.8;
`

const BadgeModalImg = styled(Box)`
  height: 55px;
  position: absolute;
  top: 35px;
  right: 25px;
`

export default class BadgeModal extends Component {
  static propTypes = {
    modalOpen: PropTypes.bool,
    badgeId: PropTypes.string,
  }

  render() {
    if (!this.props.modalOpen) {
      return null
    }

    const badgeId = this.props.badgeId
    const info = badgeInfo[badgeId]
    if (info === undefined) {
      return null
    }

    return (
      <Modal
        open
        hideBackdrop
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <BadgeModalBox>
          <Box style={{ width: 330 }}>
            <Typography variant="h6">{info.title}</Typography>
            <Typography variant="subtitle1">{info.message}</Typography>
          </Box>
          <BadgeModalImg component="img" alt={info.name} src={info.img} />
        </BadgeModalBox>
      </Modal>
    )
  }
}

export function getBadges(badges) {
  return badges.map((badge) => (
    <Box
      component="img"
      style={{ height: 45, marginRight: 15 }}
      alt={badgeInfo[badge].name}
      title={badgeInfo[badge].name}
      src={badgeInfo[badge].img}
      key={badge}
    />
  ))
}

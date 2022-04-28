import React, { Component } from 'react'
import styled from 'styled-components'

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
  render() {
    if (!this.props.modalOpen) {
      return null
    }

    const taskId = this.props.taskId
    const info = badgeInfo[taskId]

    return (
      <Modal
        open={true}
        hideBackdrop={true}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <BadgeModalBox>
          <Box style={{ width: 330 }}>
            <Typography variant="h6">{info.title}</Typography>
            <Typography variant="subtitle1">{info.message}</Typography>
          </Box>
          <BadgeModalImg component="img" alt={info.name} src={info.img}></BadgeModalImg>
        </BadgeModalBox>
      </Modal>
    )
  }
}

export function getBadges(tasks) {
  return tasks.map((task) => (
    <Box
      component="img"
      style={{ height: 45, marginRight: 15 }}
      alt={badgeInfo[task].name}
      title={badgeInfo[task].name}
      src={badgeInfo[task].img}
      key={task}
    ></Box>
  ))
}

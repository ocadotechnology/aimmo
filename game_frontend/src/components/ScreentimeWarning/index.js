import React, { useEffect } from 'react'
import styled from 'styled-components'

import { withStyles } from '@material-ui/core/styles'
import Box from '@material-ui/core/Box'
import Modal from '@material-ui/core/Modal'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'

import BrainSVG from 'img/brain.svg'
import { SettingsPowerRounded } from '@material-ui/icons'

const boxStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 410,
  bgcolor: '#ffffff',
  boxShadow: '0 0 20px rgba(0, 0, 0, .2)',
  outline: 0,
  p: 3,
}

const brainStyle = {
  width: 100,
}

// TODO: Hardcoded this for speed. We should use the shared buttons from portal when they're done.
const ContinueButton = styled(Button)({
  color: '#000000',
  borderRadius: 0,
  backgroundColor: '#ffc709',
  '&:hover': {
    backgroundColor: '#ffc709',
  },
})

const ScreentimeWarning = () => {
  const [open, setOpen] = React.useState(false) // false

  const handleContinueButton = () => {
    setOpen(false)
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      setOpen(true)
    }, 1000)
    return () => clearTimeout(timer)
  }, [])

  return (
    <Modal
      open={open}
      aria-labelledby="screentime-warning-modal-title"
      aria-describedby="screentime-warning-modal-description"
    >
      <Box css={boxStyle}>
        <Box component="img" css={brainStyle} alt="brain" src={BrainSVG} />
        <Box css={{ my: 2 }}>
          <Typography id="screentime-warning-modal-title" variant="h6" component="h2">
            Time for a break?
          </Typography>
        </Box>
        <Typography id="screentime-warning-modal-description">
          You have been using the Code for Life website for a while. Remember to take regular screen
          breaks to recharge those brain cells!
        </Typography>
        <Box css={{ mt: 2 }}>
          <ContinueButton variant="contained" onClick={handleContinueButton}>
            Continue
          </ContinueButton>
        </Box>
      </Box>
    </Modal>
  )
}

export default ScreentimeWarning

/* eslint-env jest */
import React from 'react'
import Snackbar, { StyledSnackbarContent, SnackbarContentLayout } from 'components/Snackbar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<Snackbar />', () => {
  it('renders correctly with type=success', () => {
    const tree = createShallowWithTheme(
      <Snackbar
        type='success'
        message='Snackbar message 🍿🍫'
        open
        onClose={jest.fn()}
        anchorOrigin={{ horizontal: 'left', vertical: 'up' }}
      />,
      undefined,
      true
    )
    expect(tree).toMatchSnapshot()
  })

  it('renders correctly with type=info', () => {
    const tree = createShallowWithTheme(
      <Snackbar
        type='info'
        message='Snackbar message 🍿🍫'
        open
        onClose={jest.fn()}
        anchorOrigin={{ horizontal: 'left', vertical: 'up' }}
      />,
      undefined,
      true
    )
    expect(tree).toMatchSnapshot()
  })

  it('renders correctly with type=error', () => {
    const tree = createShallowWithTheme(
      <Snackbar
        type='error'
        message='Snackbar message 🍿🍫'
        open
        onClose={jest.fn()}
        anchorOrigin={{ horizontal: 'left', vertical: 'up' }}
      />,
      undefined,
      true
    )
    expect(tree).toMatchSnapshot()
  })

  it('renders correctly with type=warning', () => {
    const tree = createShallowWithTheme(
      <Snackbar
        type='warning'
        message='Snackbar message 🍿🍫'
        open
        onClose={jest.fn()}
        anchorOrigin={{}}
      />,
      undefined,
      true
    )
    expect(tree).toMatchSnapshot()
  })
})

describe('<StyledSnackbarContent />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<StyledSnackbarContent message='Snackbar message 🍿🍫' />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<SnackbarContentLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<SnackbarContentLayout>hello</SnackbarContentLayout>)
    expect(tree).toMatchSnapshot()
  })
})

/* eslint-env jest */
import React from 'react'
import { Game } from 'containers/Game'
import { shallow } from 'enzyme'

describe('<Game />', () => {
  it('renders correctly with snackbar', () => {
    const props = {
      connectToGame: jest.fn(),
      showSnackbar: true,
      snackbarMessage: 'Snacks are the new way to keep fit'
    }
    const tree = shallow(<Game {...props} />)
    expect(tree).toMatchSnapshot()
  })

  it('renders correctly without snackbar', () => {
    const props = {
      connectToGame: jest.fn(),
      showSnackbar: false
    }
    const tree = shallow(<Game {...props} />)
    expect(tree).toMatchSnapshot()
  })
})

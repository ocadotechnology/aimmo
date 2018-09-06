/* eslint-env jest */
import React from 'react'
import { IDEEditor, IDEEditorLayout, MarginedPlayIcon, RunCodeButton } from 'components/IDEEditor'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEEditor />', () => {
  it('matches snapshot', () => {
    const props = {
      code: 'class Avatar',
      getCode: jest.fn(),
      postCode: jest.fn()
    }

    const component = createShallowWithTheme(<IDEEditor {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('calls the postCode function in props when Post code button is pressed', () => {
    const postCode = jest.fn()
    const props = {
      postCode
    }

    const component = createShallowWithTheme(<IDEEditor {...props} />, 'dark')

    component.find('#post-code-button').simulate('click')
    expect(postCode).toBeCalled()
  })
})

describe('<IDEEditorLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEEditorLayout />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<RunCodeButton />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<RunCodeButton />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

describe('<MarginedPlayIcon />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<MarginedPlayIcon />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

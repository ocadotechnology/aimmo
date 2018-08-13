/* eslint-env jest */
import React from 'react'
import IDEMenu, { IDEMenuLayout } from 'components/IDEMenu'
import { shallow } from 'enzyme'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEMenu />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEMenu />)
    expect(tree).toMatchSnapshot()
  })

  it('calls the postCode function in props when Post code button is pressed', () => {
    const postCode = jest.fn()
    const props = {
      postCode
    }

    const component = shallow(<IDEMenu {...props} />)

    component.find('#post-code-button').simulate('click')
    expect(postCode).toBeCalled()
  })
})

describe('<IDEMenuLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEMenuLayout />)
    expect(tree).toMatchSnapshot()
  })
})

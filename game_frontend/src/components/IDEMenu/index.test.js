/* eslint-env jest */
import React from 'react'
import IDEMenu from 'components/IDEMenu'
import renderer from 'react-test-renderer'
import { shallow } from 'enzyme'

describe('<IDEMenu />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<IDEMenu />).toJSON()
    expect(tree).toMatchSnapshot()
  })

  it('calls the getCode function in props when Get code button is pressed', () => {
    const getCode = jest.fn()
    const props = {
      getCode
    }

    const component = shallow(<IDEMenu {...props} />)

    component.find('#get-code-button').simulate('click')
    expect(getCode.mock.calls.length).toBe(1)
  })
})

/* eslint-env jest */
import React from 'react'
import IDEMenu from 'components/IDEMenu'
import renderer from 'react-test-renderer'

describe('<IDEMenu />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<IDEMenu></IDEMenu>).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

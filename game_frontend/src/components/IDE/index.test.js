/* eslint-env jest */
import React from 'react'
import IDE from 'components/IDE'
import renderer from 'react-test-renderer'

describe('<IDE />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<IDE></IDE>).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

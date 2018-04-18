/* eslint-env jest */
import React from 'react'
import IDEEditor from 'components/IDEEditor'
import renderer from 'react-test-renderer'

describe('<IDEEditor />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<IDEEditor code='class Avatar' />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

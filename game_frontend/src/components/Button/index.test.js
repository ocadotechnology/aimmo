/* eslint-env jest */
import React from 'react'
import Button from 'components/Button'
import renderer from 'react-test-renderer'

describe('<Button />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<Button>Button</Button>).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

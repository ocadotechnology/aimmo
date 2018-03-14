/* eslint-env jest */
import React from 'react'
import { shallow } from 'enzyme'
import Movie from 'components/Movie'
import renderer from 'react-test-renderer'

const singleMovie = {
  title: 'Test Title',
  director: 'Test Director',
  producer: 'Test Producer',
  release_date: '20/03/2018'
}

describe('<Movie />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<Movie movie={singleMovie} />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

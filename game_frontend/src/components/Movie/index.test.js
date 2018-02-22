import React from 'react'
import { shallow } from 'enzyme';
import Movie from 'components/Movie'

// The following 3 lines should be moved to a setup file
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
configure({ adapter: new Adapter() });

const singleMovie = {
  title: "Test Title",
  director: "Test Director",
  producer: "Test Producer",
  release_date: "20/03/2018"
}

describe('<Movie />', () => {
    it('should contain the string Test Title', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('Test Title')
    })
})

describe('<Movie />', () => {
    it('should contain the string Test Director', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('Test Director')
    })
})

describe('<Movie />', () => {
    it('should contain the string Test Producer', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('Test Producer')
    })
})

describe('<Movie />', () => {
    it('should contain the string 20/03/2018', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('20/03/2018')
    })
})
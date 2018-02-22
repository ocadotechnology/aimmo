import React from 'react'
import { shallow } from 'enzyme';
import Movie from 'components/Movie'
import renderer from 'react-test-renderer'

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

    it('should contain the string Test Director', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('Test Director')
    })

    it('should contain the string Test Producer', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('Test Producer')
    })

    it('should contain the string 20/03/2018', () => {
        const wrapper = shallow(<Movie movie={singleMovie} />);
        expect(wrapper.text()).toContain('20/03/2018')
    })

    it('renders correctly', () => {
        const tree = renderer.create(<Movie movie={singleMovie} />).toJSON();
        expect(tree).toMatchSnapshot();
    })
})
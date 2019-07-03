import { configure } from 'enzyme'
import Adapter from 'enzyme-adapter-react-16'
import 'jest-styled-components'

import ReactGA from 'react-ga'

ReactGA.initialize('foo', { testMode: true })

configure({ adapter: new Adapter() })

import { ajax } from 'rxjs/observable/dom/ajax'
import { API_PATH } from './constants'

const get = endpoint => {
  return ajax.getJSON(`${API_PATH}${endpoint}`, {withCredentials: true})
}

export default get

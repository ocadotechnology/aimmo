import post from './post'
import get from './get'
import unity from './unity'

export default {
  get,
  post,
  emitUnityEvent: unity.emitUnityEvent,
  sendUnityEvent: unity.sendUnityEvent,
  setGameURL: unity.setGameURL,
  setGamePath: unity.setGamePath,
  setGamePort: unity.setGamePort,
  setGameSSL: unity.setGameSSL,
  establishGameConnection: unity.establishGameConnection
}

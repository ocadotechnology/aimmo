import post from './post'
import get from './get'
import * as unity from './unity'

export default { 
    get, 
    post, 
    emitUnityEvent: unity.emitUnityEvent, 
    setGameURL: unity.setGameURL,
    setGamePath: unity.setGamePath,
    setGamePort: unity.setGamePort,
    setGameSSL: unity.setGameSSL,
    establishGameConnection: unity.establishGameConnection
}

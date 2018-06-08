import post from './post'
import get from './get'
import { 
    emitUnityEvent, 
    setGameURL, 
    setGamePath, 
    setGamePort, 
    setGameSSL, 
    establishGameConnection 
} from './unity'

export default { 
    get, 
    post, 
    emitUnityEvent, 
    setGameURL,
    setGamePath,
    setGamePort,
    setGameSSL,
    establishGameConnection
}

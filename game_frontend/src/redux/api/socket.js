import io from 'socket.io-client'
import { actions } from 'features/Game'

let socket = undefined

const connectToGame = (url, gameID, dispatch) => {
    socket = io(url, {
        path: `/game-${gameID}`
    })
    
    bindSocketEventsToActions(dispatch)
}

const bindSocketEventsToActions = (dispatch) => {
    socket.on('game-state', dispatch(actions.gameStateReceived))
}

export default { connectToGame }

import io from 'socket.io-client'

const connectToGame = (url, gameID) => {
    console.log("URL HERE: " + url + ' = ' + gameID)
    return io(url, {
        path: `/game-${gameID}`
    })
}

export default { connectToGame }

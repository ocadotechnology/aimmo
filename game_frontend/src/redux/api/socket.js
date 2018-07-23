import io from 'socket.io-client'
import actions from '../features/Game/actions'
import { map, merge } from 'rxjs/operators';
import { fromEvent } from 'rxjs/observable/fromEvent';

const connectToGame = () =>
    map(response => {
        console.log(response);
        const { game_url_base, game_id } = response;
        return io(game_url_base, {
            path: `/game-${game_id}`
        });
    });

const listenFor = (eventName, socket, action) => {
    return fromEvent(socket, eventName).pipe(
        map(event => action(event))
    );
}

const startListeners = () =>
    map(socket => {
        return merge(
          listenFor('game-state', socket, actions.socketGameStateReceived),
          // insert more events here
        )
    });


export default { connectToGame, startListeners }

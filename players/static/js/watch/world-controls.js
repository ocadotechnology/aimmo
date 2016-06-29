// World Manipulation
const CONTROLS = Object.create({
    init: function (world, viewer) {
        this.world = world;
        this.viewer = viewer;
    },
    initialiseWorld: function (width, height, worldLayout) {
        this.world.width = width;
        this.world.height = height;
        this.world.layout = worldLayout;

        this.viewer.reDrawWorldLayout();
    },
    setState: function (players, scoreLocations, pickupLocations) {
        var newPlayers = {};
        for (var key in players) {
            if (players.hasOwnProperty(key)) {
                var player = players[key];
                if (this.world.players.hasOwnProperty(key)) {
                    var oldPlayer = this.world.players[key];
                    player['oldX'] = oldPlayer.x;
                    player['oldY'] = oldPlayer.y;

                    if (player.x > oldPlayer.x) {
                        player['rotation'] = 0;
                    } else if (player.x < oldPlayer.x) {
                        player['rotation'] = Math.PI;
                    } else if (player.y > oldPlayer.y) {
                        player['rotation'] = -Math.PI / 2;
                    } else if (player.y < oldPlayer.y) {
                        player['rotation'] = Math.PI / 2;
                    } else {
                        player['rotation'] = oldPlayer['rotation'];
                    }
                } else {
                    player['rotation'] = Math.PI / 2;
                }
                newPlayers[key] = player;
            }
        }
        this.world.players = newPlayers;
        this.world.scoreLocations = scoreLocations; //TODO: use instead of relying on world.layout (and remove score from there)
        this.world.pickupLocations = pickupLocations;

        this.viewer.reDrawState();
    }
});

function refreshState(data) {
    if(data.map_changed){
        CONTROLS.initialiseWorld(data.width, data.height, data.layout);
    }
    CONTROLS.setState(data.players, data.score_locations, data.pickup_locations);
}

$(document).ready(function(){
    var world = {};
    world.players = {};
    VIEWER.init(document.getElementById("watch-world-canvas"), world, APPEARANCE);
    CONTROLS.init(world, VIEWER);

    var socket = io.connect(GAME_URL_BASE, { path: GAME_URL_PATH });
    socket.on('world-update', function(msg) {
        refreshState(msg);
  });
});

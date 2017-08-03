// World Manipulation
const CONTROLS = Object.create({
    init: function (world, viewer) {
        this.world = world;
        this.viewer = viewer;
    },
    initialiseWorld: function (width, height, worldLayout, minX, minY, maxX, maxY) {
        this.world.width = width;
        this.world.height = height;
        this.world.layout = worldLayout;
        this.world.minX = minX;
        this.world.minY = minY;
        this.world.maxX = maxX;
        this.world.maxY = maxY;

        this.viewer.reDrawWorldLayout();
    },
    setState: function (players, scoreLocations, pickups) {
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
        this.world.pickups = pickups;

        this.viewer.reDrawState();
    }
});

// Updates.
function worldUpdate(data) {
    CONTROLS.setState(data.players, data.score_locations, data.pickups);
}

// Initialisation.
function worldInit() {
    var width = 15;
    var height = 15;
    var layout = {};
    for (var x = 0; x < width; x++) {
        for (var y = 0; y < height; y++) {
            layout[x][y] = 0;
        }
    }
    var minX = -7;
    var minY = -7;
    var maxX = 7;
    var maxY = 7;

    CONTROLS.initialiseWorld(width, height, layout, minX, minY, maxX, maxY);
}

$(document).ready(function(){
    var world = {};
    world.players = {};
    VIEWER.init(document.getElementById("watch-world-canvas"), world, APPEARANCE);
    CONTROLS.init(world, VIEWER);

    if (ACTIVE) {
        var socket = io.connect(GAME_URL_BASE, { path: GAME_URL_PATH });
        socket.on('world-init'), funciton() {
            worldInit();
        }

        socket.on('world-update', function(msg) {
            worldUpdate(msg);
        });
    } /*else {
        refreshState(STATIC_DATA);
    }*/
});

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
    processUpdate: function (players, mapFeatures) {
        var i, j;

        // Create players.
        for (i = 0; i < players["create"].length; i++) {
            this.world.players.push(players["create"][i]);
        }

        // Delete players.
        for (i = 0; i < players["delete"].length; i++) {
            for (j = 0; j < this.world.players.length; j++) {
                if (this.world.players[j]["id"] === players["delete"][i]["id"]) {
                    this.world.players.splice(j, 1);
                }
            }
        }

        // Update players.
        for (i = 0; i < players["update"].length; i++) {
            for (j = 0; j < this.world.players.length; j++) {
                if (this.world.players[j]["id"] === players["update"][i]["id"]) {
                    this.world.players[j] = players["update"][i];
                }
            }
        }

        // Map features.
        var obstacles = mapFeatures["obstacle"];
        var scorePoints = mapFeatures["score_point"];
        var healthPoints = mapFeatures["health_point"];
        var pickups = mapFeatures["pickup"];

        // Create obstacles.
        for (i = 0; i < obstacles["create"].length; i++) {
            this.world.layout[obstacles["create"][i]["x"]][obstacles["create"][i]["y"]] = 1;
        }

        // Delete obstacles.
        for (i = 0; i < obstacles["delete"].length; i++) {
            this.world.layout[obstacles["delete"][i]["x"]][obstacles["delete"][i]["y"]] = 0;
        }

        // Create score points.
        for (i = 0; i < scorePoints["create"].length; i++) {
            this.world.layout[scorePoints["create"][i]["x"]][scorePoints["create"][i]["y"]] = 2;
        }

        // Delete score points.
        for (i = 0; i < scorePoints["delete"].length; i++) {
            this.world.layout[scorePoints["delete"][i]["x"]][scorePoints["delete"][i]["y"]] = 0;
        }

        // Create health points.
        for (i = 0; i < healthPoints["create"].length; i++) {
            this.world.layout[healthPoints["create"][i]["x"]][healthPoints["create"][i]["y"]] = 3;
        }

        // Delete health points.
        for (i = 0; i < healthPoints["delete"].length; i++) {
            this.world.layout[healthPoints["delete"][i]["x"]][healthPoints["delete"][i]["y"]] = 0;
        }

        // Create pickups.
        for (i = 0; i < pickups["create"].length; i++) {
            this.world.pickups.push(pickups["create"][i]);
        }

        // Delete pickups.
        for (i = 0; i < pickups["delete"].length; i++) {
            for (j = 0; j < this.world.pickups.length; j++) {
                if (this.world.pickups[j]["id"] === players["delete"][i]["id"]) {
                    this.world.pickups.splice(j, 1);
                }
            }
        }

        this.viewer.reDrawState();
    }
});

// Updates.
function worldUpdate(data) {
    CONTROLS.processUpdate(data["players"], data["map_features"]);
}

// Initialisation.
function worldInit() {
    var width = 15;
    var height = 15;
    var minX = -7;
    var minY = -7;
    var maxX = 7;
    var maxY = 7;

    var layout = {};
    for (var x = minX; x <= maxX; x++) {
        layout[x] = {};
        for (var y = minY; y <= maxY; y++) {
            layout[x][y] = 0;
        }
    }

    CONTROLS.initialiseWorld(width, height, layout, minX, minY, maxX, maxY);
}

$(document).ready(function() {

    var world = {};
    world.players = [];
    world.pickups = [];
    VIEWER.init(document.getElementById("watch-world-canvas"), world, APPEARANCE);
    CONTROLS.init(world, VIEWER);

    if (ACTIVE) {
        var socket = io.connect(GAME_URL_BASE, { path: GAME_URL_PATH });
        socket.on('world-init', function() {
            worldInit();
            socket.emit('client-ready', 1);
        });

        socket.on('world-update', function(msg) {
            worldUpdate(msg);
        });
    }
});

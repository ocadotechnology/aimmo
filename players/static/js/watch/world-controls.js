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
        var i;

        // Create players.
        for (i = 0; i < players["create"].length; i++) {
            this.world.players.push(players["create"][i]);
        }

        // Delete players.
        for (i = 0; i < players["delete"].length; i++) {
            var playerToDeleteIndex = this.world.players.indexOf(playerToDelete);
                if (playerToDeleteIndex !== -1) {
                    this.world.players.splice(playerToDeleteIndex, 1);
                }
        }

        // Update players.
        for (i = 0; i < players["update"].length; i++) {
            for (var j = 0; j < this.world.players.length; j++) {
                if (this.world.players[j]["id"] === players["update"][i]["id"]) {
                    this.world.players[j] = players["update"][i];
                }
            }
        }

        // Map features.
        var obstacles = mapFeatures["obstacle"];
        var scorePoints = mapFeatures["score_point"]
        var healthPoints = mapFeatures["health_point"]
        var pickups = mapFeatures["pickup"]

        // Create obstacles.
        for (i = 0; i < obstacles["create"].length; i++)
        {
            this.world.layout[obstacles["create"][i]["x"]][obstacles["create"][i]["y"]] = 1;
        }

        // Delete obstacles.
        for (i = 0; i < obstacles["delete"].length; i++)
        {
            this.world.layout[obstacles["delete"][i]["x"]][obstacles["delete"][i]["y"]] = 0;
        }

        // Create score points.
        for (i = 0; i < scorePoints["create"].length; i++)
        {
            this.world.layout[scorePoints["create"][i]["x"]][scorePoints["create"][i]["y"]] = 2;
        }

        // Delete score points.
        for (i = 0; i < scorePoints["delete"].length; i++)
        {
            this.world.layout[scorePoints["delete"][i]["x"]][scorePoints["delete"][i]["y"]] = 0;
        }

        this.world.pickups = [];

        this.viewer.reDrawState();
    }
});

// Updates.
function worldUpdate(data) {
    CONTROLS.processUpdate(data["players"], data["map_features"]);
}

// Initialisation.
<<<<<<< HEAD
function worldInit(data) {
    CONTROLS.initialiseWorld(data.width, data.height, data.layout, data.minX, data.minY, data.maxX, data.maxY);
=======
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
>>>>>>> acf263e... Blank map appearing on the screen. Now we need to handle updates.
}

$(document).ready(function() {

    var world = {};
    world.players = [];
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
    } /*else {
        refreshState(STATIC_DATA);
    }*/
});

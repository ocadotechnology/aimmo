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
        // Create players.
        for (var playerToCreate in players["create"]) {
            if (players["create"].hasOwnProperty(playerToCreate)) {
                if (this.world.players === null) {
                    this.world.players = {};
                }
                this.world.players.push(playerToCreate);
            }
        }

        // Delete players.
        for (var playerToDelete in players["delete"]) {
            if (players["delete"].hasOwnProperty(playerToDelete)) {
                var playerToDeleteIndex = this.world.players.indexOf(playerToDelete);
                if (playerToDeleteIndex !== -1) {
                    this.world.players.splice(playerToDeleteIndex, 1);
                }
            }
        }

        // Update players.
        for (var playerToUpdate in players["update"]) {
            if (players["update"].hasOwnProperty(playerToUpdate)) {
                var playerToUpdateIndex = this.world.players.indexOf(playerToUpdate);
                if (playerToUpdateIndex !== -1) {
                    this.world.players[playerToUpdateIndex] = playerToUpdateIndex;
                }
            }
        }

        // Map features.
        var obstacles = mapFeatures["obstacle"];
        var scorePoints = mapFeatures["score_point"]
        var healthPoints = mapFeatures["health_point"]
        var pickups = mapFeatures["pickup"]

        if (this.world.layout === null) {
            this.world.layout = {};
        }

        // Create obstacles.
        for (var obstacleToCreate in obstacles["create"])
        {
            if (obstacles["create"].hasOwnProperty(obstacleToCreate)) {
                this.world.layout[obstacleToCreate["x"]][obstacleToCreate["y"]] = 1;
            }
        }

        // Delete obstacles.
        for (var obstacleToDelete in obstacles["delete"])
        {
            if (obstacles["delete"].hasOwnProperty(obstacleToDelete)) {
                this.world.layout[obstacleToCreate["x"]][obstacleToCreate["y"]] = 0;
            }
        }

        // Create score points.
        for (var scorePointToCreate in scorePoints["create"])
        {
            if (scorePoints["create"].hasOwnProperty(scorePointToCreate)) {
                this.world.layout[scorePointToCreate["x"]][scorePointToCreate["y"]] = 2;
            }
        }

        // Delete score points.
        for (var scorePointToDelete in scorePoints["delete"])
        {
            if (scorePoints["delete"].hasOwnProperty(scorePointToDelete)) {
                this.world.layout[scorePointToDelete["x"]][scorePointToDelete["y"]] = 0;
            }
        }

        //this.world.scoreLocations = scoreLocations; //TODO: use instead of relying on world.layout (and remove score from there)
        //this.world.pickups = pickups;

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
    world.players = {};
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

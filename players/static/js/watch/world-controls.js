// World Manipulation
const CONTROLS = Object.create({
    init: function (world, viewer) {
        this.world = world;
        this.viewer = viewer;
    },
    initialiseWorld: function (minX, minY, maxX, maxY, obstacles, scoreLocations) {
        this.world.width = Math.max(maxX - minX + 1, 1);
        this.world.height = Math.max(maxY - minY + 1, 1);
        this.world.minX = minX;
        this.world.minY = minY;
        this.world.maxX = maxX;
        this.world.maxY = maxY;
        this.world.obstacles = obstacles;
        this.world.scoreLocations = scoreLocations;
        console.log(`minX: ${minX}, minY: ${minY}, maxX: ${maxX}, maxY: ${maxY} width: ${this.world.width} height: ${this.world.height}`);
        this.world.layout = this.createWorldLayout();

        this.viewer.reDrawWorldLayout();
    },
    setState: function (players, scoreLocations, pickups) {
        var newPlayers = {};
        for (var key in players) {
            if (players.hasOwnProperty(key)) {
                var player = players[key];
                if (this.world.players.hasOwnProperty(key)) {
                    var oldPlayer = this.world.players[key];
                    player['oldX'] = oldPlayer.location.x;
                    player['oldY'] = oldPlayer.location.y;

                    if (player.location.x > oldPlayer.location.x) {
                        player['rotation'] = 0;
                    } else if (player.location.x < oldPlayer.location.x) {
                        player['rotation'] = Math.PI;
                    } else if (player.location.y > oldPlayer.location.y) {
                        player['rotation'] = -Math.PI / 2;
                    } else if (player.location.y < oldPlayer.location.y) {
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
    },
    mapChanged: function(data) {
      return !(data.southWestCorner.x == this.world.minX
        && data.southWestCorner.y == this.world.minY
        && data.northEastCorner.x == this.world.maxX
        && data.northEastCorner.y == this.world.maxY)
        && this.scoreLocationsChanged(data.scoreLocations)
        && this.obstaclesChanged(data.obstacles);
    },
    scoreLocationsChanged: function(newScoreLocations) {
      return newScoreLocations.length == this.world["scoreLocations"].length
        && this.world.scoreLocations.reduce(function(acc, curr, currIndex) {
          var newLocation = newScoreLocations[currIndex].location
          return acc || !(curr.location.x == newLocation.x && curr.location.y == newLocation.y);
        }, false);
    },
    obstaclesChanged: function(newObstacles) {
      return newObstacles.length == this.world.obstacles.length
        && this.world.obstacles.reduce(function(acc, curr, currIndex) {
          var newLocation = newObstacles[currIndex].location
          return acc || !(curr.location.x == newLocation.x && curr.location.y == newLocation.y);
        }, false);
    },
    createWorldLayout: function() {
      var layout = [];
      for (var x = this.world.minX; x <= this.world.maxX; x++) {
        var columns = [];
        for (var y = this.world.minY; y <= this.world.maxY; y++) {
          columns[y] = 0;
        }
        layout[x] = columns;
      }
      console.log(layout);
      for (let obstacle of this.world.obstacles) {
        console.log(`obstacle: ${JSON.stringify(obstacle)}`);
        layout[obstacle.location.x][obstacle.location.y] = 1;
      }

      for (let scoreLocation of this.world.scoreLocations) {
        layout[scoreLocation.location.x][scoreLocation.location.y] = 2;
      }
      return layout;
    }
});

function refreshState(data) {
    // if(CONTROLS.mapChanged(data)){
        CONTROLS.initialiseWorld(data.southWestCorner.x,
          data.southWestCorner.y,
          data.northEastCorner.x,
          data.northEastCorner.y,
          data.obstacles,
          data.scoreLocations);
    // }
    CONTROLS.setState(data.players, data.scoreLocations, data.pickups);
}

$(document).ready(function(){
    var world = {
      scoreLocations: [],
      obstacles: []
    };
    world.players = {};
    VIEWER.init(document.getElementById("watch-world-canvas"), world, APPEARANCE);
    CONTROLS.init(world, VIEWER);

    if (ACTIVE) {
        var socket = io.connect(GAME_URL_BASE, { path: GAME_URL_PATH });
        socket.on('game-state', function(msg) {
            refreshState(msg);
        });
    } else {
        refreshState(STATIC_DATA);
    }
});

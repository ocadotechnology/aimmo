// All calls to paper.* should call invertY to get from simulation coordinate system into visualisation coordinate system, then scale up by appearance.cellSize

const APPEARANCE = Object.create({
    cellSize: 50,
    worldColours: {
        "GRASS": "#efe",
        "WALL": "#777",
        "SCORE": "#fbb"
    }
});

const VIEWER = Object.create({
    init: function(canvasDomElement, world, appearance) {
        this.world = world;
        this.appearance = appearance;
        this.paper = Raphael(canvasDomElement);
    },

    drawnElements: {
        players: [],
        pickups: [],
    },

    invertY: function(height, y) {
        if(y == undefined) {
            debugger;
        }
        return height - y - 1;
    },

    reDrawWorldLayout: function(world) {
        var self = this;
        self.paper.clear();
        self.paper.setViewBox(0, 0, world.width * self.appearance.cellSize, world.height * self.appearance.cellSize, true);
        for (x = 0; x < world.width; x++) {
            for (y = 0; y < world.height; y++) {
                currentCellValue = world.layout[x][y];

                var square = self.paper.rect(x * self.appearance.cellSize,
                    self.invertY(world.height, y) * self.appearance.cellSize,
                    self.appearance.cellSize,
                    self.appearance.cellSize);

                square.attr("fill", self.appearance.worldColours[currentCellValue]);
                square.attr("stroke", "#000");

                self.paper.text((x + 0.5) * self.appearance.cellSize, (self.invertY(world.height, y) + 0.5) * self.appearance.cellSize, x + ', ' + y)
            }
        }
    },

    constructNewPlayerElement: function(playerData, height) {
        const playerX = (0.5 + playerData.x) * this.appearance.cellSize;
        const playerY = (0.5 + this.invertY(height, playerData.y)) * this.appearance.cellSize;
        const playerRadius = this.appearance.cellSize * 0.5 * 0.75;
        const playerHeadRadius = playerRadius * 0.6;
        const playerEyeRadius = playerRadius * 0.2;

        var playerBody = this.paper.circle(playerX, playerY, playerRadius);

        playerBody.attr("fill", playerData.colours.bodyFill);
        playerBody.attr("stroke", playerData.colours.bodyStroke);
        var playerEyeLeft = this.paper.circle(
            playerX + playerHeadRadius * Math.cos(playerData.rotation - 1),
            playerY + playerHeadRadius * Math.sin(playerData.rotation - 1),
            playerEyeRadius
        );

        playerEyeLeft.attr("fill", playerData.colours.eyeFill);
        playerEyeLeft.attr("stroke", playerData.colours.eyeStroke);
        var playerEyeRight = this.paper.circle(
            playerX + playerHeadRadius * Math.cos(playerData.rotation + 1),
            playerY + playerHeadRadius * Math.sin(playerData.rotation + 1),
            playerEyeRadius
        );

        playerEyeRight.attr("fill", playerData.colours.eyeFill);
        playerEyeRight.attr("stroke", playerData.colours.eyeStroke);

        var playerTextAbove = this.paper.text(playerX, playerY - 20, 'Score: ' + playerData.score);
        var playerTextBelow = this.paper.text(playerX, playerY + 20, playerData.health + 'hp, (' + playerData.x + ', ' + playerData.y + ')');

        var player = this.paper.set();
        player.push(
            playerBody,
            playerEyeLeft,
            playerEyeRight,
            playerTextAbove,
            playerTextBelow
        );
        return player;
    },

    clearDrawnElements: function(elements) {
        elements.forEach(function(elementToRemove) {
            elementToRemove.remove();
        });
    },

    reDrawPlayers: function(players, height) {
        var self = this;
        return Object.keys(players).map(function(playerKey) {
            var playerData = players[playerKey];
            return self.constructNewPlayerElement(playerData, height);
        });
    },

    reDrawPickups: function(pickupLocations, height) {
        var self = this;
        return pickupLocations.map(function(pickupLocation, i) {
            var x = (0.5 + pickupLocation[0]) * self.appearance.cellSize;
            var y = (0.5 + self.invertY(height, pickupLocation[1])) * self.appearance.cellSize;
            var radius = self.appearance.cellSize * 0.5 * 0.75;
            var circle = self.paper.circle(x, y, radius);
            circle.attr("fill", '#FFFFFF');
            var crossX = self.paper.rect(x - 10, y - 3, 20, 6).attr({fill: '#FF0000', stroke: '#FF0000'});
            var crossY = self.paper.rect(x - 3, y - 10, 6, 20).attr({fill: '#FF0000', stroke: '#FF0000'});
            var pickup = self.paper.set();
            pickup.push(circle, crossX, crossY);
            return pickup;
        });
    },

    reDrawState: function(drawnElements, world) {
        this.clearDrawnElements(drawnElements.pickups);
        this.clearDrawnElements(drawnElements.players);
        return {
            drawnElements: {
                pickups: this.reDrawPickups(world.pickupLocations, world.height),
                players: this.reDrawPlayers(world.players, world.height),
            },
            height: world.height,
        };
    }
});
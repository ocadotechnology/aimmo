// All calls to paper.* should call invertY to get from simulation coordinate system into visualisation coordinate system, then scale up by appearance.cellSize
'use strict';
(function () {
    var raphael = window.Raphael; // not a constructor?

    // TODO can CSS help eleminate these magic numbers?
    window.APPEARANCE = {
        cellSize: 50,
        crossLengthScaleFactor: 0.4,
        crossWidthScaleFactor: 0.12,
        playerTextOffsetScaleFactor: 0.4,
        pickupScaleFactor: 0.5 * 0.75,
        playerScaleFactor: 0.5 * 0.6,
        playerHeadScaleFactor: 0.6,
        playerEyeScaleFactor: 0.2,
        playerEyeOffsetRadians: 1, // TODO would Math.PI / 4  or Math.PI / 6 make more sense?
        worldColours: {
            HEALTH_CROSS: "#ff0000",
            HEALTH_BACKGROUND: '#FFFFFF',
            GRASS: "#efe",
            WALL: "#777",
            SCORE: "#fbb",
            BODY_STROKE: "#0FF",
            EYE_STROKE: "#AFF",
            EYE_FILL: "#EFF",
            CELL_STROKE: "#000",
            PLAYERS: [
               "#B58900",
               "#CB4B16",
               "#DC322F",
               "#D33682",
               "#6C71C4",
               "#268BD2",
               "#2AA1982AA198"
            ]
        }
    };

    window.Viewer = function (canvasDomElement, appearance) {
        this.appearance = appearance;
        this.paper = raphael(canvasDomElement);
    };

    window.Viewer.prototype = {};

    window.Viewer.prototype.invertY = function (height, y) {
        return height - y - 1;
    };

    window.Viewer.prototype.reDrawWorldLayout = function (world) {
        var self = this,
            width = world.layout.length;
        self.paper.clear();
        self.paper.setViewBox(0, 0, width * self.appearance.cellSize, world.height * self.appearance.cellSize, true);
        world.layout.forEach(function (row, x) {
            row.forEach(function (currentCellValue, y) {

                var square = self.paper.rect(x * self.appearance.cellSize,
                    self.invertY(world.height, y) * self.appearance.cellSize,
                    self.appearance.cellSize,
                    self.appearance.cellSize);

                square.attr("fill", self.appearance.worldColours[currentCellValue]);
                square.attr("stroke", self.appearance.worldColours.CELL_STROKE);

                self.paper.text((x + 0.5) * self.appearance.cellSize,
                    (self.invertY(world.height, y) + 0.5) * self.appearance.cellSize, x + ', ' + y);
            });
        });
    };

    window.Viewer.prototype.constructNewPlayerElement = function (playerData, height) {
        function cycle(arr, i) {
            var index = i % arr.length;
            return arr[index];
        }
        var self = this,
            playerX = (0.5 + playerData.x) * this.appearance.cellSize,
            playerY = (0.5 + this.invertY(height, playerData.y)) * this.appearance.cellSize,
            playerRadius = this.appearance.cellSize * this.appearance.playerScaleFactor,
            playerHeadRadius = playerRadius * this.appearance.playerHeadScaleFactor,
            playerEyeRadius = playerRadius * this.appearance.playerEyeScaleFactor,
            playerBody = this.paper.circle(playerX, playerY, playerRadius),
            directionToRotationRadians = {
                SOUTH: Math.PI / 2,
                EAST: 0,
                NORTH: -Math.PI / 2,
                WEST: Math.PI,

            },
            rotationRadians = directionToRotationRadians[playerData.lastMove],
            leftEyeAngle = rotationRadians - self.appearance.playerEyeOffsetRadians,
            rightEyeAngle = rotationRadians + self.appearance.playerEyeOffsetRadians,
            playerEyeLeft = this.paper.circle(
                playerX + playerHeadRadius * Math.cos(leftEyeAngle),
                playerY + playerHeadRadius * Math.sin(leftEyeAngle),
                playerEyeRadius
            ),
            playerEyeRight = this.paper.circle(
                playerX + playerHeadRadius * Math.cos(rightEyeAngle),
                playerY + playerHeadRadius * Math.sin(rightEyeAngle),
                playerEyeRadius
            ),
            playerTextAbove = this.paper.text(
                playerX,
                playerY - self.appearance.playerTextOffsetScaleFactor * self.appearance.cellSize,
                'Score: ' + playerData.score
            ),
            playerTextBelow = this.paper.text(
                playerX,
                playerY + self.appearance.playerTextOffsetScaleFactor * self.appearance.cellSize,
                playerData.health + 'hp, (' + playerData.x + ', ' + playerData.y + ')'
            ),
            player = this.paper.set(),
            playerBodyCol = this.appearance.worldColours.PLAYERS[playerData.customization % 5],
            playerEdgeCol = this.appearance.worldColours.PLAYERS[~~(playerData.customization / 5)];

        playerBody.attr("fill", playerBodyCol);
        playerBody.attr("stroke", playerEdgeCol);
        playerBody.attr("stroke-width", 5);

        [playerEyeLeft, playerEyeRight].forEach(function(eye) {
            eye.attr("fill", playerEdgeCol);
           eye.attr("stroke-width", 0);
        });

        player.push(
            playerBody,
            playerEyeLeft,
            playerEyeRight,
            playerTextAbove,
            playerTextBelow
        );
        return player;
    };

    window.Viewer.prototype.clearDrawnElements = function (elements) {
        elements.forEach(function (elementToRemove) {
            elementToRemove.remove();
        });
    };

    window.Viewer.prototype.reDrawPlayers = function (players, height) {
        var self = this;
        // TODO how to know which color is which player?
        // Should indicate some sort of a key.
        // Also how does the player know their own ID?
        // It doesn't match their login name.
        return Object.keys(players).map(function (playerKey, i) {
            var playerData = players[playerKey];
            playerData.index = i;
            return self.constructNewPlayerElement(playerData, height);
        });
    };

    window.Viewer.prototype.reDrawPickups = function (pickupLocations, height) {
        var self = this;
        return pickupLocations.map(function (pickupLocation) {
            var x = (0.5 + pickupLocation[0]) * self.appearance.cellSize,
                y = (0.5 + self.invertY(height, pickupLocation[1])) * self.appearance.cellSize,
                radius = self.appearance.cellSize * self.appearance.pickupScaleFactor,
                circle = self.paper.circle(x, y, radius),
                crossX = self.paper.rect(
                    x - (self.appearance.crossLengthScaleFactor * self.appearance.cellSize / 2),
                    y - (self.appearance.crossWidthScaleFactor * self.appearance.cellSize / 2),
                    self.appearance.crossLengthScaleFactor * self.appearance.cellSize,
                    self.appearance.crossWidthScaleFactor * self.appearance.cellSize).attr({

                    fill: self.appearance.worldColours.HEALTH_CROSS,
                    stroke: self.appearance.worldColours.HEALTH_CROSS
                }),
                crossY = self.paper.rect(
                    x - (self.appearance.crossWidthScaleFactor * self.appearance.cellSize / 2),
                    y - (self.appearance.crossLengthScaleFactor * self.appearance.cellSize / 2),
                    self.appearance.crossWidthScaleFactor * self.appearance.cellSize,
                    self.appearance.crossLengthScaleFactor * self.appearance.cellSize).attr({
                    fill: self.appearance.worldColours.HEALTH_CROSS,
                    stroke: self.appearance.worldColours.HEALTH_CROSS,
                }),
                pickup = self.paper.set();

            circle.attr("fill", self.appearance.worldColours.HEALTH_BACKGROUND);
            pickup.push(circle, crossX, crossY);
            return pickup;
        });
    };

    window.Viewer.prototype.reDrawState = function (drawnElements, world) {
        this.clearDrawnElements(drawnElements.pickups);
        this.clearDrawnElements(drawnElements.players);
        return {
            drawnElements: {
                pickups: this.reDrawPickups(world.pickupLocations, world.height),
                players: this.reDrawPlayers(world.players, world.height),
            },
            height: world.height,
        };
    };
}());

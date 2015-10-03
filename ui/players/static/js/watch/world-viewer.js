// All calls to paper.* should call invertY to get from simulation coordinate system into visualisation coordinate system, then scale up by appearance.cellSize
'use strict';
(function () {
    var raphael = window.Raphael; // TODO not a constructor?

    // TODO can CSS help eleminate these magic numbers?
    window.APPEARANCE = Object.create({
        cellSize: 50,
        pickupScaleFactor: 0.5 * 0.75,
        playerScaleFactor: 0.5 * 0.75,
        playerHeadScaleFactor: 0.6,
        playerEyeScaleFactor: 0.2,
        playerEyeOffset: 1,
        playerTextOffset: 20,
        worldColours: {
            HEALTH_CROSS: "#ff0000",
            HEALTH_BACKGROUND: '#FFFFFF',
            GRASS: "#efe",
            WALL: "#777",
            SCORE: "#fbb",
            BODY_STROKE: "#0FF",
            EYE_STROKE: "#AFF",
            EYE_FILL: "#EFF",
            PLAYERS: [
               "#001387",
               "#00270e",
               "#003A95",
               "#004E1C",
               "#0061A3",
               "#00752A"
            ]
        }
    });
    window.VIEWER = Object.create({
        init: function (canvasDomElement, appearance) {
            this.appearance = appearance;
            this.paper = raphael(canvasDomElement);
        },

        invertY: function (height, y) {
            return height - y - 1;
        },

        reDrawWorldLayout: function (world) {
            var self = this;
            self.paper.clear();
            self.paper.setViewBox(0, 0, world.width * self.appearance.cellSize, world.height * self.appearance.cellSize, true);
            world.layout.forEach(function (row, x) {
                row.forEach(function (currentCellValue, y) {

                    var square = self.paper.rect(x * self.appearance.cellSize,
                        self.invertY(world.height, y) * self.appearance.cellSize,
                        self.appearance.cellSize,
                        self.appearance.cellSize);

                    square.attr("fill", self.appearance.worldColours[currentCellValue]);
                    square.attr("stroke", "#000");

                    self.paper.text((x + 0.5) * self.appearance.cellSize,
                        (self.invertY(world.height, y) + 0.5) * self.appearance.cellSize, x + ', ' + y);
                });
            });
        },

        constructNewPlayerElement: function (playerData, height) {
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
                leftEyeAngle = playerData.rotation - self.appearance.playerEyeOffset,
                rightEyeAngle = playerData.rotation + self.appearance.playerEyeOffset,
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
                playerTextAbove = this.paper.text(playerX, playerY - self.appearance.playerTextOffset, 'Score: ' + playerData.score),
                playerTextBelow = this.paper.text(playerX, playerY + self.appearance.playerTextOffset, playerData.health + 'hp, (' + playerData.x + ', ' + playerData.y + ')'),
                player = this.paper.set(),
                playerColor = cycle(this.appearance.worldColours.PLAYERS, playerData.id);
            console.log("Player color", playerColor);

            playerBody.attr("fill", playerColor);
            playerBody.attr("stroke", this.appearance.BODY_STROKE);

            [playerEyeLeft, playerEyeRight].forEach(function(eye) {
                eye.attr("fill", self.appearance.worldColours.EYE_FILL);
                eye.attr("stroke", self.appearance.worldColours.EYE_STROKE);
            });

            player.push(
                playerBody,
                playerEyeLeft,
                playerEyeRight,
                playerTextAbove,
                playerTextBelow
            );
            return player;
        },

        clearDrawnElements: function (elements) {
            elements.forEach(function (elementToRemove) {
                elementToRemove.remove();
            });
        },

        reDrawPlayers: function (players, height) {
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
        },

        reDrawPickups: function (pickupLocations, height) {
            var self = this;
            return pickupLocations.map(function (pickupLocation) {
                var x = (0.5 + pickupLocation[0]) * self.appearance.cellSize,
                    y = (0.5 + self.invertY(height, pickupLocation[1])) * self.appearance.cellSize,
                    radius = self.appearance.cellSize * self.appearance.pickupScaleFactor,
                    circle = self.paper.circle(x, y, radius),
                    crossX = self.paper.rect(x - 10, y - 3, 20, 6).attr({
                        fill: self.appearance.worldColours.HEALTH_CROSS,
                        stroke: self.appearance.worldColours.HEALTH_CROSS
                    }),
                    crossY = self.paper.rect(x - 3, y - 10, 6, 20).attr({
                        fill: self.appearance.worldColours.HEALTH_CROSS,
                        stroke: self.appearance.worldColours.HEALTH_CROSS,
                    }),
                    pickup = self.paper.set();

                circle.attr("fill", self.appearance.worldColours.HEALTH_BACKGROUND);
                pickup.push(circle, crossX, crossY);
                return pickup;
            });
        },

        reDrawState: function (drawnElements, world) {
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
}());
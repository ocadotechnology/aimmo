// All calls to paper.* should call invertY to get from simulation coordinate system into visualisation coordinate system, then scale up by appearance.cellSize

const VIEWER = Object.create(
    {
        world : null,
        appearance : null,
        paper : null,

        drawnElements : {
            drawnPlayers : [],
            drawnItems : []
        },

        init : function(canvasDomElement, world, appearance) {
            this.world = world;
            this.appearance = appearance;
            this.paper = Raphael(canvasDomElement);
        },

        invertY : function(y) {
            return this.world.height - y - 1;
        },

        reDrawWorldLayout : function() {
            const world = this.world;
            const paper = this.paper;

            paper.clear();
            this.drawnElements.drawnPlayers = [];
            this.drawnElements.drawnItems = [];


            paper.setViewBox(0, 0, world.width * this.appearance.cellSize, world.height * this.appearance.cellSize, true);

            for (var x = 0; x < world.width; x++) {
                for (var y = 0; y < world.height; y++) {
                    var currentCellValue = world.layout[x][y];

                    var square = paper.rect(x * this.appearance.cellSize,
                        this.invertY(y) * this.appearance.cellSize,
                        this.appearance.cellSize,
                        this.appearance.cellSize);

                    square.attr("fill", this.appearance.worldColours[currentCellValue]);
                    square.attr("stroke", "#000");

                    paper.text((x + 0.5) * this.appearance.cellSize,  (this.invertY(y) + 0.5) * this.appearance.cellSize, x + ', ' + y)
                }
            }
        },

        constructNewPlayerElement : function(playerData) {
            const playerX = (0.5 + playerData.x) * this.appearance.cellSize;
            const playerY = (0.5 + this.invertY(playerData.y)) * this.appearance.cellSize;
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

            var playerText = this.paper.text(playerX, playerY + 20, playerData.health + 'hp, (' + playerData.x + ', ' + playerData.y + ')');

            var player = this.paper.set();
            player.push(
                playerBody,
                playerEyeLeft,
                playerEyeRight,
                playerText
            );
            return player;
        },

        reDrawPlayers : function() {
            const world = this.world;
            const paper = this.paper;

            while (this.drawnElements.drawnPlayers.length > 0) {
                var elementToRemove = this.drawnElements.drawnPlayers.pop();
                elementToRemove.remove();
            }

            for (var playerKey in world.players) {
                var playerData = world.players[playerKey];
                var playerElement = this.constructNewPlayerElement(playerData);
                this.drawnElements.drawnPlayers.push(playerElement);
            }
        },

        reDrawItems : function() {
            const world = this.world;
            const paper = this.paper;
        },

        reDrawState : function() {
            this.reDrawItems();
            this.reDrawPlayers();
        }
    }
);
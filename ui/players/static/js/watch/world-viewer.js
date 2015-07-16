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
            this.appearance = appearance
            this.paper = Raphael(canvasDomElement);
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
                    var currentCellValue = world.layout[y][x];

                    var square = paper.rect(x * this.appearance.cellSize,
                        y * this.appearance.cellSize,
                        this.appearance.cellSize,
                        this.appearance.cellSize);

                    square.attr("fill", this.appearance.worldColours[currentCellValue]);
                    square.attr("stroke", "#000");
                }
            }
        },

        constructNewPlayerElement : function(playerData) {
            const playerX = (0.5 + playerData.x) * this.appearance.cellSize;
            const playerY = (0.5 + playerData.y) * this.appearance.cellSize;
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


            var player = this.paper.set();
            player.push(
                playerBody,
                playerEyeLeft,
                playerEyeRight
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
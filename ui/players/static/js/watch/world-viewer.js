const VIEWER = Object.create(
    {
        world : null,
        paper : null,

        parameters : {
            squareWidth : 50,
            worldColours : {
                0 : "#fff",
                1 : "#777"
            }
        },

        drawnElements : {
            drawnPlayers : [],
            drawnItems : []
        },

        init : function(canvasDomElement, world) {
            this.world = world;
            this.paper = Raphael(canvasDomElement);
        },

        drawWorldLayout : function() {
            const world = this.world;
            const paper = this.paper;

            paper.clear();
            paper.setViewBox(0, 0, world.width * this.parameters.squareWidth, world.height * this.parameters.squareWidth, true);

            for (var x = 0; x < world.width; x++) {
                for (var y = 0; y < world.height; y++) {
                    var currentCellValue = world.layout[y][x];

                    var square = paper.rect(x * this.parameters.squareWidth,
                        y * this.parameters.squareWidth,
                        this.parameters.squareWidth,
                        this.parameters.squareWidth);

                    square.attr("fill", this.parameters.worldColours[currentCellValue]);
                    square.attr("stroke", "#000");
                }
            }
        },

        constructNewPlayerElement : function(playerData) {
            const playerX = (0.5 + playerData.x) * this.parameters.squareWidth;
            const playerY = (0.5 + playerData.y) * this.parameters.squareWidth;
            const playerRadius = this.parameters.squareWidth * 0.5 * 0.75;
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

            for (var playerKey = 0; playerKey < world.players.length; playerKey++) {
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
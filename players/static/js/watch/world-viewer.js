// All calls to paper.* should call invertY to get from simulation coordinate system into visualisation coordinate system, then scale up by appearance.cellSize

const APPEARANCE = Object.create({
    cellSize: 50,
    worldColours: {
        0: "#efe",
        1: "#777",
        2: "#fbb",
        3: "#ade"
    }
});

const VIEWER = Object.create({
    drawnElements: {
        players: [],
        pickups: []
    },

    init: function(canvasDomElement, world, appearance) {
        this.world = world;
        this.appearance = appearance;
        this.paper = Raphael(canvasDomElement);
    },

    invertY: function(y) {
        return -y;
    },

    reDrawWorldLayout: function() {
        this.paper.clear();
        this.paper.setViewBox(this.world.minX * this.appearance.cellSize, this.world.minY * this.appearance.cellSize,           //min possible coordinates
                              this.world.width * this.appearance.cellSize, this.world.height * this.appearance.cellSize,        //size of grid
                              true);

        for (var x = this.world.minX; x <= this.world.maxX; x++) {
            for (var y = this.world.minY; y <= this.world.maxY; y++) {
                var currentCellValue = this.world.layout[x][y];

                var square = this.paper.rect(x * this.appearance.cellSize,
                    this.invertY(y) * this.appearance.cellSize,
                    this.appearance.cellSize,
                    this.appearance.cellSize);

                square.attr("fill", this.appearance.worldColours[currentCellValue]);
                square.attr("stroke", "#000");

                this.paper.text((x + 0.5) * this.appearance.cellSize,  (this.invertY(y) + 0.5) * this.appearance.cellSize, x + ', ' + y)
            }
        }
    },

    constructNewPlayerElement: function(playerData, is_current_user) {
        const playerX = (0.5 + playerData["x"]) * this.appearance.cellSize;
        const playerY = (0.5 + this.invertY(playerData["y"])) * this.appearance.cellSize;
        const playerRadius = this.appearance.cellSize * 0.5 * 0.75;
        const currentUserIconSize = playerRadius * 0.4;

        var playerBody = this.paper.circle(playerX, playerY, playerRadius);

        playerBody.attr("fill", "#6495ED");
        playerBody.attr("stroke", "#6495ED");

        var currentUserIcon;
        if (is_current_user) {
            currentUserIcon = this.paper.rect(
                playerX - currentUserIconSize / 2,
                playerY - currentUserIconSize / 2,
                currentUserIconSize,
                currentUserIconSize
            );
            currentUserIcon.attr("fill", "#FF0000");
            currentUserIcon.attr("stroke", "#FF0000");
        }

        var playerTextAbove = this.paper.text(playerX, playerY - 20, 'Score: ' + playerData["score"]);
        var playerTextBelow = this.paper.text(playerX, playerY + 20, playerData["health"] + 'hp, (' + playerData["x"] + ', ' + playerData["y"] + ')');

        var player = this.paper.set();
        player.push(
            playerBody,
            playerTextAbove,
            playerTextBelow,
            currentUserIcon
        );
        return player;
    },

    clearDrawnElements: function(elements) {
        while (elements.length > 0) {
            var elementToRemove = elements.pop();
            elementToRemove.remove();
        }
    },

    reDrawPlayers: function() {
        this.clearDrawnElements(this.drawnElements.players);

        for (var i = 0;  i < this.world.players.length; i++) {
            var is_current_user = this.world.players[i]["id"] === CURRENT_USER_PLAYER_KEY;
            var playerElement = this.constructNewPlayerElement(this.world.players[i], is_current_user);
            this.drawnElements.players.push(playerElement);
        }
    },

    reDrawPickups: function() {
        this.clearDrawnElements(this.drawnElements.pickups);

        for (var i = 0; i < this.world.pickups.length; i++) {
            var pickupLocation = this.world.pickups[i].location;
            var x = (0.5 + pickupLocation[0]) * this.appearance.cellSize;
            var y = (0.5 + this.invertY(pickupLocation[1])) * this.appearance.cellSize;

            // Just for testing.
            pickup = this.drawHealth(x, y);
        }
    },

    drawHealth: function(x, y) {
        var radius = this.appearance.cellSize * 0.5 * 0.75;
        var circle = this.paper.circle(x, y, radius);
        circle.attr("fill", '#FFFFFF');
        var crossX = this.paper.rect(x - 10, y - 3, 20, 6).attr({fill: '#FF0000', stroke: '#FF0000'});
        var crossY = this.paper.rect(x - 3, y - 10, 6, 20).attr({fill: '#FF0000', stroke: '#FF0000'});
        var pickup = this.paper.set();
        pickup.push(circle, crossX, crossY);
        return pickup;
    },

    drawInvulnerability: function(x, y) {
        var radius = this.appearance.cellSize * 0.5 * 0.75;
        var circle = this.paper.circle(x, y, radius);
        circle.attr('fill', '#0066ff');
        var pickup = this.paper.set();
        pickup.push(circle);
        return pickup;
    },

    drawDamage: function(x, y) {
        var radius = this.appearance.cellSize * 0.5 * 0.75;
        var circle = this.paper.circle(x, y, radius);
        circle.attr('fill', '#ff0000');
        var pickup = this.paper.set();
        pickup.push(circle);
        return pickup;
    },

    reDrawState: function() {
        this.reDrawWorldLayout();
        this.reDrawPickups();
        this.reDrawPlayers();
    }
});

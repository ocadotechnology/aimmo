// World Manipulation
const CONTROLS = Object.create({
    init: function (world, viewer) {
        this.world = world;
        this.viewer = viewer;
    },

    initialiseWorld: function (width, height, worldLayout) {
        this.world.width = width;
        this.world.height = height;
        this.world.layout = worldLayout;

        this.viewer.reDrawWorldLayout();
    },
    setState: function (players, scoreLocations) {
        this.world.players = players;
        this.world.scoreLocations = scoreLocations;

        this.viewer.reDrawState();
    }
});

function refreshState() {
    $.ajax("/api/watch/state", {
        success : function(data) {
            if(data.map_changed){
                CONTROLS.initialiseWorld(data.width, data.height, data.layout);
            }
            CONTROLS.setState(data.players, data.score_locations);
            setTimeout(refreshState, 200);
        },
        error : function(jqXHR, textStatus, errorThrown) {
            setTimeout(refreshState, 500);
        }
    });
}

$(function(){
    var world = {};
    VIEWER.init(document.getElementById("watch-world-canvas"), world, APPEARANCE);
    CONTROLS.init(world, VIEWER);

    refreshState();
});
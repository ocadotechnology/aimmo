// World Manipulation
const CONTROLS = Object.create({
    init: function (world, viewer) {
        this.world = world;
        this.viewer = viewer;
    },

    initialiseWorld: function (width, height, worldLayout) {
        // TODO is width/height ever incosnistent with layout?!
        this.viewer.reDrawWorldLayout({width: width, height: height, layout: worldLayout});
    },
    setState: function (players, scoreLocations, pickupLocations) {
        this.viewer.drawnElements = this.viewer.reDrawState({players: players, pickupLocations: pickupLocations});
    }
});

function refreshState() {
    $.ajax("/api/watch/state", {
        success : function(data) {
            if(data.map_changed){
                CONTROLS.initialiseWorld(data.width, data.height, data.layout);
            }
            CONTROLS.setState(data.players, data.score_locations, data.pickup_locations);
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
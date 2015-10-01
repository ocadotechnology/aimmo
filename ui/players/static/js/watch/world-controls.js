// World Manipulation
const CONTROLS = Object.create({
    init: function (world, viewer) {
        this.world = world;
        this.viewer = viewer;
    },

    initialiseWorld: function (width, height, worldLayout) {
        // TODO is width/height ever incosnistent with layout?!
        this.viewer.reDrawWorldLayout({width: width, height: height, layout: worldLayout});
        return height;
    },
    setState: function (players, scoreLocations, pickupLocations, height, drawnElements) {
        return this.viewer.reDrawState(drawnElements, 
            {players: players, pickupLocations: pickupLocations, height: height});
    }
});

function jsonAsync(url, timeout) {
    return new Promise(function(res, rej) {
        setTimeout(function() {
            $.ajax(url, {
                success: function(data) {
                    res(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    rej({jqXHR: jqXHR, textStatus: textStatus, errorThrown: errorThrown});
                }
            });
        }, timeout);
    });
};

function refreshState(eventualState) {
    // TODO should be 500ms timeout for error.
    var newPromise = Promise.all([eventualState, jsonAsync("/api/watch/state", 200)]).then(function(arr) {
        var data = arr[1];
        var height = data.map_changed ?
            CONTROLS.initialiseWorld(data.width, data.height, data.layout) :
            arr[0].height;
        return CONTROLS.setState(data.players,
            data.score_locations,
            data.pickup_locations,
            height,
            arr[0].drawnElements);
    }).catch(function(er) {
        console.error(er);
        return eventualState;
    });
    setTimeout(function() {refreshState(newPromise)}, 0);

};

$(function(){
    var world = {};
    var eventualState = Promise.resolve({drawnElements: {players: [], pickups: []}});
    VIEWER.init(document.getElementById("watch-world-canvas"), world, APPEARANCE);
    CONTROLS.init(world, VIEWER);
    refreshState(eventualState);
});
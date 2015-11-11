// World Manipulation
'use strict';
(function () {
    var Promise = window.Promise,
        $ = window.$;

    function jsonAsync(url) {
        return new Promise(function (res, rej) {
            $.ajax(url, {
                success: function (data) {
                    res(data);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    rej({jqXHR: jqXHR, textStatus: textStatus, errorThrown: errorThrown});
                }
            });
        });
    }

    window.CONTROLS = Object.create({
        init: function (viewer) {
            this.viewer = viewer;
        },

        initialiseWorld: function (width, height, worldLayout) {
            // TODO is width/height ever incosnistent with layout?!
            this.viewer.reDrawWorldLayout({width: width, height: height, layout: worldLayout});
            return height;
        },
        setState: function (players, pickupLocations, height, drawnElements) {
            return this.viewer.reDrawState(drawnElements,
                {players: players, pickupLocations: pickupLocations, height: height});
        }
    });


    window.refreshState = function (eventualState) {
        var newPromise = Promise.all([eventualState, jsonAsync("/api/watch/state")]).then(function (arr) {
            var data = arr[1],
                height = data.map_changed ?
                        CONTROLS.initialiseWorld(data.width, data.height, data.layout) :
                        arr[0].height,
                output = CONTROLS.setState(data.players,
                    data.pickup_locations,
                    height,
                    arr[0].drawnElements);
            setTimeout(function () { window.refreshState(output); }, 200);
        }).catch(function (er) {
            console.error(er);
            setTimeout(function () { window.refreshState(eventualState); }, 500);
        });
    };

}());

window.$(function () {
    var VIEWER = window.VIEWER,
        APPEARANCE = window.APPEARANCE,
        CONTROLS = window.CONTROLS,
        Promise = window.Promise,
        refreshState = window.refreshState,
        eventualState = Promise.resolve({drawnElements: {players: [], pickups: []}});

    VIEWER.init(document.getElementById("watch-world-canvas"), APPEARANCE);
    CONTROLS.init(VIEWER);
    refreshState(eventualState);
});

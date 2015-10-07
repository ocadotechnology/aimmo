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

    window.Controls = function (viewer) {
        this.viewer = viewer;
    };

    window.Controls.prototype = {};

    window.Controls.prototype.initialiseWorld = function (width, height, worldLayout) {
       // TODO is width/height ever incosnistent with layout?!
        this.viewer.reDrawWorldLayout({width: width, height: height, layout: worldLayout});
        return height;
    };

    window.Controls.prototype.setState = function (players, pickupLocations, height, drawnElements) {
        return this.viewer.reDrawState(drawnElements,
            {players: players, pickupLocations: pickupLocations, height: height});
    };


    window.refreshState = function (controls, eventualState) {
        var newPromise = Promise.all([eventualState, jsonAsync("/api/watch/state")]).then(function (arr) {
            var data = arr[1],
                height = data.map_changed ?
                        controls.initialiseWorld(data.width, data.height, data.layout) :
                        arr[0].height,
                output = controls.setState(data.players,
                    data.pickup_locations,
                    height,
                    arr[0].drawnElements);
            setTimeout(function () { window.refreshState(controls, output); }, 200);
        }).catch(function (er) {
            console.error(er);
            setTimeout(function () { window.refreshState(controls, eventualState); }, 500);
        });
    };

}());

window.$(function () {
    var Viewer = window.Viewer,
        APPEARANCE = window.APPEARANCE,
        Controls = window.Controls,
        Promise = window.Promise,
        refreshState = window.refreshState,
        eventualState = Promise.resolve({drawnElements: {players: [], pickups: []}}),
        viewer = new Viewer(document.getElementById("watch-world-canvas"), APPEARANCE),
        controls = new Controls(viewer);

    refreshState(controls, eventualState);
});

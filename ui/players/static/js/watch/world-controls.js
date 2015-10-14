/*jslint browser: true*/
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

    window.refreshState = function (viewer, state) {
        debugger;
        jsonAsync("/api/watch/state").then(function (data) {
            var height = data.map_changed ?
                            viewer.reDrawWorldLayout(data.layout) :
                            state.height,
                world = {
                    pickupLocations: data.pickup_locations,
                    height: height,
                    players: data.players
                },
                output = viewer.reDrawState(state.drawnElements, world);
            setTimeout(function () { window.refreshState(viewer, output); }, 500);
        }).catch(function (er) {
            var didSuccessfullyRender = $("svg > text").length,
                status = didSuccessfullyRender ? "LOST_CONNECTION" : "GAME_NOT_STARTED",
                showAlert = window.showAlert;
            console.error(er);
            showAlert({status: status});
        });
    };

}());

window.$(function () {
    var Viewer = window.Viewer,
        APPEARANCE = window.APPEARANCE,
        Promise = window.Promise,
        refreshState = window.refreshState,
        initialState = {drawnElements: {players: [], pickups: []}},
        viewer = new Viewer(document.getElementById("watch-world-canvas"), APPEARANCE);

    refreshState(viewer, initialState);
});

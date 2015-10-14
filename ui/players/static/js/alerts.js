'use strict';
(function () {
    var messages = messages = {
        OK: "Your game was successfully saved.",
        USER_ERROR: "Your code has some problems:",
        GAME_NOT_STARTED: "The game has not started yet. Please start the game.",
        UNKNOWN_ERROR: "Could not connect to the game. Try refreshing the page?",
        COULD_NOT_RETRIEVE_SAVED_DATA: "Could not retrieve saved data.",
        ERROR_OCCURRED_WHILST_SAVING: "An error occurred whilst saving.",
        save: "Save",
        description: "Use the box below to program your Avatar. Save using the button on the right.",
    };

    function showAlert(data) {
        var alerts = $('#alerts'),
            outer = $('#aimmo-alert-message-outer'),
            inner = $('#aimmo-alert-message-inner');

        alerts.toggleClass('alert-success', data.status === "OK");
        alerts.toggleClass('alert-danger', data.status !== "OK");

        if (data.message) {
            outer.show();
            if (data.message.constructor === Array) {
                data.message.forEach(function (stackframe) {
                    var div = $("<div>");
                    div.text(stackframe.trim());
                    inner.append(div);
                });
            } else {
                inner.text(data.message);
            }
        } else {
            outer.hide();
        }

        $('#aimmo-alert-text').text(messages[data.status] || messages.UNKNOWN_ERROR);
        $('#alerts').show();
    }

    window.showAlert = showAlert;
}());
'use strict';
(function () {
    var messages = window.messages.statuses;

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
                    inner.append("<div>" + stackframe.trim() + "<div>");
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
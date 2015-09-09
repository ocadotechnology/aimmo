$( document ).ready(function() {
    var defaultProgram = "print 'Hello, world!'\nprint 'New line'";

    var messages = {
        OK: "Your game was successfully saved.",
        USER_ERROR: "Your code has some problems:",
        GAME_NOT_STARTED: "The game has not started yet. Please start the game.",
        UNKNOWN_ERROR: "Could not connect to the game. Try refreshing the page?",
        COULD_NOT_RETRIEVE_SAVED_DATA: "Could not retrieve saved data.",
        ERROR_OCCURRED_WHILST_SAVING: "An error occurred whilst saving.",
    };

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    var setButtonsEnabled = function(enableStatus){
        $('#saveBtn').prop('disabled', !enableStatus);
    };

    var startsWith = function(string, prefix) {
        // Triple equals?
        return string.slice(0, prefix.length) === prefix;
    };

    var showAlert = function(data) {
        var alertText = $('#alerts');
        var alerts = $('#alerts');
        var outer = $('#aimmo-alert-message-outer');
        var inner = $('#aimmo-alert-message-inner');

        alerts.toggleClass('alert-success', data.status === "OK");
        alerts.toggleClass('alert-danger', data.status !== "OK");

        if(data.message) {
          outer.show();
            if(data.message.constructor === Array) {
                data.message.forEach(function(stackframe) {
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
    };

    $.ajax({
        //TODO - get URL
        url: '/api/code/',
        type: 'GET',
        dataType: 'text',
        success: function(data) {
            editor.setValue(data);
            editor.selection.moveCursorFileStart();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            showAlert({status: COULD_NOT_RETRIEVE_SAVED_DATA});
            editor.setValue(defaultProgram);
            editor.selection.moveCursorFileStart();
        }
    });

    $('#saveBtn').click(function(event){
        event.preventDefault();
        $.ajax({
            //TODO - get URL
            url: '/api/code/',
            type: 'POST',
            data: {code: editor.getValue(), csrfmiddlewaretoken: $('#saveForm input[name=csrfmiddlewaretoken]').val()},
            success: function(data) {
                $('#alerts').hide();
                showAlert(JSON.parse(data));
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert({status: ERROR_OCCURRED_WHILST_SAVING, message: errorThrown});
            }
        });
    });
});
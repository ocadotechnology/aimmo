'use strict';
window.$(function () {
    var $ = window.$,
        ace = window.ace,
        messages = {
            OK: "Your game was successfully saved.",
            USER_ERROR: "Your code has some problems:",
            GAME_NOT_STARTED: "The game has not started yet. Please start the game.",
            UNKNOWN_ERROR: "Could not connect to the game. Try refreshing the page?",
            COULD_NOT_RETRIEVE_SAVED_DATA: "Could not retrieve saved data.",
            ERROR_OCCURRED_WHILST_SAVING: "An error occurred whilst saving.",
        },
        editor = ace.edit("editor");


    $('#saveBtn').attr('value', messages.save);
    $('#aimmo-program-description').text(messages.description);

    editor.$blockScrolling = Infinity;
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.setReadOnly(true);

    $.ajax({
        //TODO - get URL
        url: '/api/code/',
        type: 'GET',
        dataType: 'text',
        success: function (data) {
            editor.setValue(data);
            editor.setReadOnly(false);
            editor.selection.moveCursorFileStart();
        },
        error: function () {
            showAlert({status: 'COULD_NOT_RETRIEVE_SAVED_DATA'});
            editor.selection.moveCursorFileStart();
        }
    });

    $('#saveBtn').click(function (event) {
        event.preventDefault();
        $.ajax({
            //TODO - get URL
            url: '/api/code/',
            type: 'POST',
            data: {code: editor.getValue(), csrfmiddlewaretoken: $('#saveForm input[name=csrfmiddlewaretoken]').val()},
            success: function (data) {
                $('#alerts').hide();
                showAlert(JSON.parse(data));
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert({status: 'ERROR_OCCURRED_WHILST_SAVING', message: errorThrown});
            }
        });
    });
});
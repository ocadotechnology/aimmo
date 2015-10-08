'use strict';
window.$(function () {
    var $ = window.$,
        ace = window.ace,
        showAlert = window.showAlert,
        messages = window.messages.program,
        defaultProgram = "print 'Hello, world!'\nprint 'New line'",
        editor = ace.edit("editor");


    $('#saveBtn').attr('value', messages.save);
    $('#aimmo-program-description').text(messages.description);

    editor.$blockScrolling = Infinity;
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    $.ajax({
        //TODO - get URL
        url: '/api/code/',
        type: 'GET',
        dataType: 'text',
        success: function (data) {
            editor.setValue(data);
            editor.selection.moveCursorFileStart();
        },
        error: function () {
            showAlert({status: 'COULD_NOT_RETRIEVE_SAVED_DATA'});
            editor.setValue(defaultProgram);
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
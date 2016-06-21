$( document ).ready(function() {
    const DANGER_CLASS = 'alert-danger';
    const SUCCESS_CLASS = 'alert-success';

    var defaultProgram = "print 'Sorry, could not retrieve saved data'\n";

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    var showAlert = function(alertString, alertType) {
        if (alertType === DANGER_CLASS || alertType === SUCCESS_CLASS) {
            var alertText = $('#alerts');
            alertText.removeClass('alert-success alert-danger');
            alertText.addClass(alertType);
            alertText.html(alertString + '<button type="button" class="close" aria-hidden="true">x</button>');
            $(".close").click(function(){
                alertText.hide();
            });
            alertText.show();
        }
    };

    const StatusCode = Object.freeze({
        "SUCCESS": function(message) { showAlert('Success:<br/><br/>' + message, SUCCESS_CLASS); },
        "SERVER_ERROR": function(message) { showAlert(message, DANGER_CLASS); },
        "USER_ERROR": function(message) { showAlert('Your code has some problems:<br/><br/>' + message, DANGER_CLASS); },
    });

    var checkStatus = function(data) {
        if (data != undefined && StatusCode[data.status] != undefined) {
            return StatusCode[data.status](data.message);
        } else {
            return showAlert('An unknown error has occurred whilst saving:', DANGER_CLASS);
        }
    };

    $.ajax({
        url: Urls['aimmo/code'](),
        type: 'GET',
        dataType: 'text',
        success: function(data) {
            editor.setValue(data);
            editor.selection.moveCursorFileStart();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            showAlert('Could not retrieve saved data', DANGER_CLASS);
            editor.setValue(defaultProgram);
            editor.selection.moveCursorFileStart();
        }
    });

    $('#saveBtn').click(function(event) {
        event.preventDefault();
        $.ajax({
            url: Urls['aimmo/code'](),
            type: 'POST',
            dataType: 'json',
            data: {code: editor.getValue(), csrfmiddlewaretoken: $('#saveForm input[name=csrfmiddlewaretoken]').val()},
            success: function(data) {
                $('#alerts').hide();
                checkStatus(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert('An error has occurred whilst saving: ' + errorThrown, DANGER_CLASS);
            }
        });
    });
});

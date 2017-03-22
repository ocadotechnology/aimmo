

$( document ).ready(function() {
    //CONSTANTS
    const DANGER_CLASS = 'alert-danger';
    const SUCCESS_CLASS = 'alert-success';
    const defaultProgram = "print 'Sorry, could not retrieve saved data'\n";


    const StatusCode = Object.freeze({
        "SUCCESS": function(message) { showAlert('Success:<br/><br/>' + message, SUCCESS_CLASS); },
        "SERVER_ERROR": function(message) { showAlert(message, DANGER_CLASS); },
        "USER_ERROR": function(message) { showAlert('Your code has some problems:<br/><br/>' + message, DANGER_CLASS); },
    });

    //HELPER FUNCTIONS
    function showAlert (alertString, alertType) {
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
    }

    // trigger extension
    ace.require("ace/ext/language_tools");
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    // enable autocompletion and snippets
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
    });

    var checkStatus = function(data) {
        if (data != undefined && StatusCode[data.status] != undefined) {
            return StatusCode[data.status](data.message);
        } else {
            return showAlert('An unknown error has occurred whilst saving:', DANGER_CLASS);
        }
    };

    //EVENTS
    $('#saveBtn').click(function(event) {
        event.preventDefault();
        $.ajax({
            url: Urls['aimmo/code'](id=GAME_ID),
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

    //DISPLAY CODE
    $.ajax({
        url: Urls['aimmo/code'](id=GAME_ID),
        type: 'GET',
        dataType: 'text',
        success: function(data) {
            editor.setValue(data);
            editor.selection.moveCursorFileStart();
            editor.setReadOnly(false);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            showAlert('Could not retrieve saved data', DANGER_CLASS);
            editor.setValue(defaultProgram);
            editor.selection.moveCursorFileStart();
            editor.setReadOnly(true);
        }
    });

});



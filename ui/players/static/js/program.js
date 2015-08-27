$( document ).ready(function() {
    var defaultProgram = "print 'Hello, world!'\nprint 'New line'";

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    var setButtonsEnabled = function(enableStatus){
        $('#saveBtn').prop('disabled', !enableStatus);
    };

    var startsWith = function(string, prefix) {
        return string.slice(0, prefix.length) == prefix;
    };

    var showAlert = function(alertString){
        var alertText = $('#alerts');
        alertText.html(alertString + '<button type="button" class="close" aria-hidden="true">x</button>');
        $(".close").click(function(){
            alertText.hide();
        });
        alertText.show();
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
            showAlert('Could not retrieve saved data');
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

                const USER_ERROR_RESPONSE = "USER_ERROR\n\n";
                const SERVER_ERROR_RESPONSE = "SERVER_ERROR\n\n";
                if (data == "OK") {
                  // do nothing
                } else if (startsWith(data, USER_ERROR_RESPONSE)) {
                    showAlert('Your code has some problems:<br/><br/>' + data.slice(USER_ERROR_RESPONSE.length, data.length));
                } else if (startsWith(data, SERVER_ERROR_RESPONSE)) {
                    showAlert(data.slice(SERVER_ERROR_RESPONSE.length, data.length));
                } else {
                    showAlert('Unknown response from server');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert('An error has occurred whilst saving:' + errorThrown);
            }
        });
    });
});
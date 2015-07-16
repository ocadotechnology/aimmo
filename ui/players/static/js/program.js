$( document ).ready(function() {

    var defaultProgram = "print 'Hello, world!'\nprint 'New line'";

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    var setButtonsEnabled = function(enableStatus){
        $('#saveBtn').prop('disabled', !enableStatus);
    };
    
    var showAlert = function(alert){
        var alertText = $('#alerts');
        alertText.html(alert);
        alertText.show();
    };

    $.ajax({
        //TODO - get URL
        url: 'http://localhost:1111/this-doesnt-exist',
        type: 'GET',
        dataType: 'text',
        success: function(data) {
            editor.setValue(data);
            editor.selection.moveCursorFileStart();
            editor.getSession().on('change', function(e) {
                setButtonsEnabled(true);
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            showAlert('Could not retrieve saved data');
            editor.setValue(defaultProgram);
            editor.selection.moveCursorFileStart();
            editor.getSession().on('change', function(e) {
                setButtonsEnabled(true);
            });
        }       
    });

    $('#saveBtn').click(function(){
        $.ajax({
            //TODO - get URL
            url: 'http://localhost:1111/this-doesnt-exist',
            type: 'POST',
            data: 'text',
            success: function(data) {
                setButtonsEnabled(false);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert('An error has occurred whilst saving: ' + errorThrown);
                
            }       
        });
    });

    
});
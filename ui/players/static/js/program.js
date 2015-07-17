$( document ).ready(function() {

    var defaultProgram = "print 'Hello, world!'\nprint 'New line'";

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    var setButtonsEnabled = function(enableStatus){
        $('#saveBtn').prop('disabled', !enableStatus);
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

    $('#saveBtn').click(function(event){
        event.preventDefault();
        $.ajax({
            //TODO - get URL
            url: '/api/code/',
            type: 'POST',
            data: {code: editor.getValue(), csrfmiddlewaretoken: $('#saveForm input[name=csrfmiddlewaretoken]').val()},
            success: function(data) {
                setButtonsEnabled(false);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                showAlert('An error has occurred whilst saving: ' + errorThrown);
                
            }       
        });
    });

    
});
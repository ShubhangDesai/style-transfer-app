$(function() {
    $('#stylize-button').click(function() {
        $.ajax({
            url: '/stylize',
            type: 'GET',
            success: function(response) {
              window.location.replace("/result");
            },
            error: function(error) {
              console.log(error);
            }
        });
    });
});

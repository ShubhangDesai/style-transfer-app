$(function() {
    $('#test').click(function() {
        console.log("alsdfj2")
        $.ajax({
            url: '/stylize',
            type: 'GET',
            success: function(response) {
              console.log("wfow")
              console.log(typeof(response))
              $('#img').attr("src", response)
            },
            error: function(error) {
              console.log(error);
            }
        });
    });
});

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

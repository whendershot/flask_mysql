$(document).ready(function() {

    $('#users').change(function(){
        $.ajax({
            type : 'GET',
            url : '/friendships/_get_potential/',
            data : {selected_user : $('#users').val()},
            success : function(data) {
                $('#potential_friends').html(data.html_string);
                }
        });
    });
});
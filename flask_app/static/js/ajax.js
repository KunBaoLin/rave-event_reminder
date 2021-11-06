console.log('Coding');
$(document).ready(function(){ 
    $("#element-form-ajax").submit(function(e){
        e.preventDefault();
        var response = $.post('/rave/create/ajax',$('#element-form-ajax').serialize());
        console.log('RESPONSE HERE: ${response}');
        response.done(function(data){
            console.log('DATA HERE: ${data}');
            $('#all-events').append(data)
        })
    })
});
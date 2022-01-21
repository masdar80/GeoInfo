$(document).ready(function(){

$('.show-form').click(function(){
$.ajax({
url:'create_rdd/',
type:'get',
dataType:'json',
beforeSend:function(){
$('#rdd-modal').modal('show');
},
success:function(data){
$('#rdd-modal .modal-content').html(data[html_form]);
}

});
});

});
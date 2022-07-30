$(document).on('submit','#capture',function(e)
         {
e.preventDefault();
$.ajax({
type:'POST',
url:'/capture',
data:{},
success:function()
{
alert('saved');
}
})
});

$(document).on('submit','#startscan',function(e)
         {
$(".btn-success").attr("disabled",true);
$(".btn-primary").attr("disabled",true);
$(".btn-danger").attr("disabled",false);
e.preventDefault();
$.ajax({
type:'POST',
url:'/startscan',
data:{},
success:function()
{
console.log('started');
}

})
});



$(document).on('submit','#stopscan',function(e)
         {
$(".btn-success").attr("disabled",false);
$(".btn-primary").attr("disabled",false);
$(".btn-danger").attr("disabled",true);
e.preventDefault();
$.ajax({
type:'POST',
url:'/stopscan',
data:{},
success:function()
{
console.log('stopped');
}
})
});

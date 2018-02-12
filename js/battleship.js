$(document).ready(function() {
  var socket = io.connect('http://127.0.0.1:5000');
  
  socket.on('connect', function() {
  });

  socket.on('message', function(msg) {
    console.log(msg)
    $("#messages").append('<li><b>'+msg.name+':</b> '+msg.message+'</li>');
  });

  $('#sendbutton').on('click', function() {
    socket.send({
      name: $('#name').val(),
      message:$('#message').val(),
      type:"chat"
    });
  });
});

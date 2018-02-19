$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  
  console.log(socket)
  
  socket.on('connect', function() {
    console.log("connected");
  });

  socket.on('message', function(msg) {
    console.log(msg)
    $("#messages").append('<li><b>'+msg.name+':</b> '+msg.message+'</li>');
  });

  $('#sendbutton').on('click', function() {
    socket.send({
      type:"chat",
      name: $('#name').val(),
      message:$('#message').val()
    });
  });
});

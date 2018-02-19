$(document).ready(function() {
  var socket = io.connect('ws://' + document.domain + ':' + location.port + '/ws');

  var mySocket = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

  mySocket.onopen = function (event) {
  };
  

  mySocket.onmessage = function(event) {
    console.log(event.data);
    msg = JSON.parse(event.data);
    $("#messages").append('<li><b>'+msg.name+':</b> '+msg.message+'</li>');
  };

  $('#sendbutton').on('click', function() {
    mySocket.send(JSON.stringify({
      type:"chat",
      name: $('#name').val(),
      message:$('#message').val()
    }));
  });
});

$(document).ready(function() {

  var socket = io.connect( 'http://' + document.domain + ':' + location.port );

  for (var i = 1; i <= 100; i++) {
    // The number and letter designators
    if (i < 11) {
      $(".top").prepend("<span class='aTops'>" + Math.abs(i - 11) + "</span>");
      $(".bottom").prepend("<span class='aTops'>" + Math.abs(i - 11) + "</span>");
      $(".grid").append("<li class='points offset1 " + i + "'><span class='hole'></span></li>");
    } else {
      $(".grid").append("<li class='points offset2 " + i + "'><span class='hole'></span></li>");
    }
    if (i == 11) {
      $(".top").prepend("<span class='aTops hidezero'>" + Math.abs(i - 11) + "</span>");
      $(".bottom").prepend("<span class='aTops hidezero'>" + Math.abs(i - 11) + "</span>");
    }
    if (i > 90) {
      $(".top").append("<span class='aLeft'>" + 
                String.fromCharCode(97 + (i - 91)).toUpperCase() + "</span>");
      $(".bottom").append("<span class='aLeft'>" + 
                String.fromCharCode(97 + (i - 91)).toUpperCase() + "</span>");
    }
  };
  
  socket.on('connect', function() {
  });

  socket.on('message', function(msg) {
    if (msg.type == "chat")
      $("#messages").append('<li><b>'+msg.name+':</b> '+msg.message+'</li>');
  });

  $('#sendbutton').on('click', function() {
    socket.send({
      name: $('#name').val(),
      message:$('#message').val(),
      type:"chat"
    });
    $('#message').val("");
  });
});

// Variables
var playerFleet, cpuFleet;
var attemptedHits = [];

// Object Constructors
function Fleet(name) {
  this.name = name;
  this.shipDetails = [{ "name": "carrier", "length": 5 },
            { "name": "battleship", "length": 4 },
            { "name": "cruiser", "length": 3 },
            { "name": "destroyer", "length": 3 },
            { "name": "frigate", "length": 2 }];
  this.numOfShips = this.shipDetails.length;
  this.ships = [];
  this.currentShipSize = 0;
  this.currentShip = 0;
  this.initShips = function() {
    for(var i = 0; i < this.numOfShips; i++) {
      this.ships[i] = new Ship(this.shipDetails[i].name);
      this.ships[i].length = this.shipDetails[i].length;
    }
  };
  this.removeShip = function(pos) {
    this.numOfShips--;
    $(".text").text(output.sunk(this.name, this.ships[pos].name));
    if (this == playerFleet) bot.sizeOfShipSunk = this.ships[pos].length;
    this.ships.splice(pos, 1);
    if (this.ships.length == 0) {
      $(".text").text(output.lost(this.name));
    }
    return true;
  };
  this.shipHit = function(ship_name) {
    $(".text").text(output.hit(this.name));
    return true;
  }
  this.checkIfHit = function(point) {
    for(var i = 0; i < this.numOfShips; i++) {
      if (this.ships[i].checkLocation(point)) {
        this.ships[i].getRidOf(this.ships[i].hitPoints.indexOf(point));
        if (this.ships[i].hitPoints == 0)return this.removeShip(i);
        else return this.shipHit(this.ships[i].name);
      }
    }
    return false;
  };
}

function Ship(name){
  this.name = name;
  this.length = 0;
  this.hitPoints = [];
  this.populateHorzHits = function(start) {
    for (var i = 0; i < this.length; i++, start++) {
      this.hitPoints[i] = start;
    }
  };
  this.populateVertHits = function(start) {
    for (var i = 0; i < this.length; i++, start += 10) {
      this.hitPoints[i] = start;
    }
  };
  this.checkLocation = function(loc) {
    for (var i = 0; i < this.length; i++) {
      if (this.hitPoints[i] == loc) return true;    
    }
    return false;
  };
  this.getRidOf = function(pos) {
    this.hitPoints.splice(pos, 1);
  }
}

// Objects for playing the game and bot for playing the computer
var topBoard = {
  allHits: [],
  highlight: function(square) {
    $(square).addClass("target").off("mouseleave").on("mouseleave", function() {
      $(this).removeClass("target"); 
    });

    $(square).off("click").on("click", function() {
      if(!($(this).hasClass("used"))) {
        $(this).removeClass("target").addClass("used");
        var num = parseInt($(this).attr("class").slice(15));
        var bool = cpuFleet.checkIfHit(num);
        if (false == bool) {
          $(".text").text(output.miss("You"));
          $(this).children().addClass("miss");
        } else $(this).children().addClass("hit");
        $(".top").find(".points").off("mouseenter").off("mouseover").off("mouseleave").off("click");
        // Check if it's the end of the game
        if (cpuFleet.ships.length == 0) {
          $(".top").find(".points").off("mouseenter").off("mouseover").off("mouseleave").off("click");

        } else setTimeout(bot.select, 800);
      } // end of if
    });
  },
}

var bottomBoard = {
  currentHits: [],
  checkAttempt: function(hit) {
    if (playerFleet.checkIfHit(hit)) {
      // Insert hit into an array for book keeping
      bottomBoard.currentHits.push(hit);
      if (this.currentHits.length > 1) bot.prev_hit = true;
      // display hit on the grid
      $(".bottom").find("." + hit).children().addClass("hit");
      if (bottomBoard.hasShipBeenSunk()) {
        // clear flags
        bot.hunting = bot.prev_hit = false;
        if (bot.sizeOfShipSunk == bottomBoard.currentHits.length) {
          bot.num_misses = bot.back_count = bot.nextMove.length = bottomBoard.currentHits.length = bot.sizeOfShipSunk = bot.currrent = 0;
        } else {
          bot.special =  bot.case1 = true;
        }
        // check for special cases
        if (bot.specialHits.length > 0) bot.special = true;
        // check for end of game. 
      }
      return true;
    } else {
      $(".bottom").find("." + hit).children().addClass("miss");
      bot.current = bottomBoard.currentHits[0];
      bot.prev_hit = false;
      if (bottomBoard.currentHits.length > 1) {
        bot.back = true;
        bot.num_misses++;
      }
      if (bot.case2) {
        bot.special = true;
        bot.case2 = false;
      }
      return false;
    }
  },

  hasShipBeenSunk: function() {
    if (bot.sizeOfShipSunk > 0) return true;
    else return false;
  }
}
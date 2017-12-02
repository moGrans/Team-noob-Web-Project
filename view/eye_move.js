// cdpn.io/rkcjt
// https://codepen.io/sergep/pen/rkcjt
// // If you use this code, please link to this pen (cdpn.io/rkcjt). Thanks :)

var DrawEye = function(eyecontainer, pupil, eyeposx, eyeposy){
	// Initialise variables
  	var r = $(pupil).width()/2;
  	var center = {
    	x: $(eyecontainer).width()/2 - r, 
    	y: $(eyecontainer).height()/2 - r
  	};
  	var distanceThreshold = $(eyecontainer).width()/2 - r;
  	var mouseX = 0, mouseY = 0;
  
  	// Listen for mouse movement
  	$(window).mousemove(function(e){ 
    	var d = {
      		x: e.pageX - r - eyeposx - center.x,
      		y: e.pageY - r - eyeposy - center.y
    	};
    	var distance = Math.sqrt(d.x*d.x + d.y*d.y);
    	if (distance < distanceThreshold) {
      		mouseX = e.pageX - eyeposx - r;
      		mouseY = e.pageY - eyeposy - r;
    	} else {
      		mouseX = d.x / distance * distanceThreshold + center.x;
      		mouseY = d.y / distance * distanceThreshold + center.y;
    	}
  	});
  
  	// Update pupil location
  	var pupil = $(pupil);
  	var xp = 0, yp = 0;
  	var loop = setInterval(function(){
   		// change 1 to alter damping/momentum - higher is slower
    	xp += (mouseX - xp) / 1;
    	yp += (mouseY - yp) / 1;
    	pupil.css({left:xp, top:yp});    
  	}, 1);
};

var pariseye1 = new DrawEye("#eyeleft", "#pupilleft", 155, 800);


var DrawEye = function(eyecontainer, eyepupil, speed, interval){
  var mouseX = 0, mouseY = 0, xp = 0, yp = 0;
  var limitX = $(eyecontainer).width() - $(eyepupil).width(),
      limitY = $(eyecontainer).height() - $(eyepupil).height(),
      offset = $(eyecontainer).offset();

  $(window).mousemove(function(e){
    mouseX = Math.min(e.pageX - offset.left, limitX);
    mouseY = Math.min(e.pageY - offset.top, limitY);
    if (mouseX < 0) mouseX = 0;
    if (mouseY < 0) mouseY = 0;
  });

  var follower = $(eyepupil);
  var loop = setInterval(function(){
    xp += (mouseX - xp) / speed;
    yp += (mouseY - yp) / speed;
    follower.css({left:xp, top:yp});
  }, interval);
};

//create eyes
var eye1 = new DrawEye("#left-eye",  "#left-pupil", 8, 30);
var eye2 = new DrawEye("#right-eye", "#right-pupil", 8, 30);  
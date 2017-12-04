window.onload = function() {
	var bone = document.getElementById("mouse_follower");
	document.addEventListener("mousemove", getMouse); 

	bone.style.position = "absolute"; //css		
	var bonepos = {x:0, y:0};

	setInterval(followMouse, 50);

	var mouse = {x:0, y:0}; //mouse.x, mouse.y

	var dir = "right";
	function getMouse(e){
		mouse.x = e.pageX;
		mouse.y = e.pageY;
		//Checking directional change
		if(mouse.x > bonepos.x){
  			dir = "left";
			} else {
  			dir = "right";
		}
	}

	function followMouse(){
		//1. find distance X , distance Y
		var distX = mouse.x - bonepos.x;
		var distY = mouse.y - bonepos.y;
		//Easing motion
		bonepos.x += distX/5;
		bonepos.y += distY/2;
		
		bone.style.left = bonepos.x + "px";
		bone.style.top = bonepos.y + "px";
  
        //Apply css class 
        if (dir == "right"){
          bone.setAttribute("class", "mouse_follow_right");
        } else {
          bone.setAttribute("class", "mouse_follow_left");        
        }	
	}
}
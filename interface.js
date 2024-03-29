var host = "ws://127.0.0.1:8765/",
    ws_host="",
    img_host="http://192.168.1.110:8081/",
    ws,
    invert_x =  1,
    invert_y = -1,
    invert_z = -1,
    killCode = 0,
    key_x = 0,
    key_y = 0;
    key_trigger = 0,
    isClicked=0;
    selectedJoystick=0;

function getIP(){
  re = /(\d+\.){3}\d+/;
  ip = re.exec(document.URL);
  try{
    if(ip[0]){ document.getElementById("host").value = ip[0]; }
  }
  catch(err){ console.log("Failed to find IP"); }
}

function updateHost(){
  host=document.getElementById("host").value;
  //img_host = "http://"+ host +":8081/";
  ws_host = "ws://"+ host +":8765/";
  console.log("WS Host: "+ws_host);
  //document.getElementById("host").value = host;
  //document.getElementById("vid_window").src= img_host;
  ws = new WebSocket(ws_host);
  ws.onmessage = function(event) {
    if( event.data != '' ){
      console.log( event.data ); 
      updateBattery( event.data );  
    } 
  };
pollBattInterval = setInterval(pollBattery, 1000);
}

function setLimit(speed){
  try{ if(ws.readyState==1){ ws.send("limit,"+speed); } }
  catch(err) { console.log("Error setting speed limit"); }
}

function setOutput(button){
  if(button == 0){
    if(!prevTrigger){
      prevTrigger = 1;
      try{ if(ws.readyState==1){ ws.send("button,"+button); } }
      catch(err) { }
    }
  }
  else{
    if(!prevButton2){
      prevButton2 = 1;
      try{ if(ws.readyState==1){ ws.send("button,"+button); } }
      catch(err) { }
    }
  }
}

function selectJoystick(){
  selectedJoystick = document.forms[0].elements["Joystick"].selectedIndex;
  console.log(selectedJoystick);
}

function keyDownListen(key){
  //console.log(key.key);
  switch( key.key ){
  case "ArrowUp":
    key_y = 1;
    break;
  case "ArrowDown":
    key_y = -1;
    break;
  case "ArrowRight":
    key_x = 1;
    break;
  case "ArrowLeft":
    key_x = -1;
    break;
  case " ":
    key_trigger = 1;
    break;
  }
}

function keyUpListen(key){
  switch( key.key ){
  case "ArrowUp":
    key_y = 0;
    break;
  case "ArrowDown":
    key_y = 0;
    break;
  case "ArrowRight":
    key_x = 0;
    break;
  case "ArrowLeft":
    key_x = 0;
    break;
  case " ":
    key_trigger = 0;
    break;
  }
}

function updateStick(){
  var x=0, y=0, z=0, trigger = 0;
  try{
    var gamepads = navigator.getGamepads();
    x = gamepads[selectedJoystick]["axes"][0]*invert_x;
    y = gamepads[selectedJoystick]["axes"][1]*invert_y;
    z = gamepads[selectedJoystick]["axes"][2]*invert_z;
    trigger = gamepads[selectedJoystick]["buttons"][0]["pressed"];
  }
  catch(err){  }
  if(  key_x != 0 ){ x = key_x; }
  if(  key_y != 0 ){ y = key_y; }
  if(  key_trigger != 0 ){ trigger = key_trigger; }
  return [x,y,z,trigger];
}

function mouseHandler(handleEvent){
  console.log(handleEvent);
}

function drawScreen(){
    var cursor_color="#00ff00";
    var [x,y,z,trigger] = updateStick();
//          if(ws.readystate!=1){ ws = new WebSocket(host); }
    try{ if(ws.readyState==1){ ws.send( "drive,"+x+","+y+","+z+","+trigger ); } }
    catch(err) { }
    document.getElementById("xy_axis").style.left=x*250+250;
    document.getElementById("xy_axis").style.bottom=y*250+250;
    if(trigger){ cursor_color="#FF0000"; }
    document.getElementById("xy_axis").style.backgroundColor=cursor_color;
}

function listGamepads(){
  var gamepads=navigator.getGamepads();
  for(i=0;i<gamepads.length;i++){
    if(gamepads[i]!=null){
      document.forms[0].elements["Joystick"].innerHTML='';
      console.log( gamepads[i]);
      document.forms[0].elements["Joystick"].add(new Option(gamepads[i]["id"],i));
    }
  }
}

function mouseDriveInit(){
  //Mouse driving code
  driveBox = document.getElementById("driveBox") ;
  rect = driveBox.getBoundingClientRect();
  driveBox.addEventListener('touchstart', e=> {
    //e.preventDefault();
    isClicked = 1;
    console.log("CLICK");
  });
  driveBox.addEventListener('mousedown', e=> {
    isClicked = 1;
    console.log("CLICK");
  });
  driveBox.addEventListener('touchmove', e=> {
    //e.preventDefault();
    if(isClicked){
      x = (e.touches[0].clientX - 250 - rect.left )/250.0 ;
      y = -( e.touches[0].clientY - rect.top - 250 )/250.0;
      if ( -1 < x && x < 1 ){ key_x = x; }
      if ( -1 < y && y < 1 ){ key_y = y; }
      //key_y = (250 - e.clientY - rect.top  )/250.0;
      console.log(key_x+ "," +key_y);
    }
  });
  driveBox.addEventListener('mousemove', e=> {
    if(isClicked){
      key_x = (e.clientX - 250 - rect.left )/250.0 ;
      key_y = -( e.clientY - rect.top - 250 )/250.0;
      console.log(key_x+ "," +key_y);
    }
  });
  document.addEventListener('touchend', e=> {
    isClicked = 0;
    key_x = 0;
    key_y = 0;
  });
  document.addEventListener('mouseup', e=> {
    isClicked = 0;
    key_x = 0;
    key_y = 0;
  });
}

function pageInit(){
  getIP();
  setTimeout(listGamepads,500);
  killCode = setInterval(drawScreen, 50);
  mouseDriveInit();
}

function updateBattery( vbatt ){
  document.getElementById("voltage").innerHTML = vbatt;
}

function pollBattery(){
  if( ws.readyState == 1 ){
    ws.send("battery");
  }
}

document.onkeydown = keyDownListen;
document.onkeyup = keyUpListen;
document.addEventListener("DOMContentLoaded", pageInit, false);

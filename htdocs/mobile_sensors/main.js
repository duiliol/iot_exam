var state
var i=0
var sensor
var hostname = "192.168.1.191"
var port = "1883"
var clientId = ""
var mqttClient = new Paho.MQTT.Client(hostname, port, clientId);
mqttClient.onMessageArrived = messageArrived;

function messageArrived(message){

}

function form_handler()
{}

function mainEdge(){
    document.getElementById("cloudButton").setAttribute("hidden","true");
    x=sensor.x;
    y=sensor.y;
    z=sensor.z;
    var module = Math.sqrt(Math.pow(x,2)+Math.pow(x,2)+Math.pow(x,2));
    document.getElementById("activityHeader").innerHTML="Current activity";
    if(module>2){
        document.getElementById("activity").setAttribute("style","color:yellow");
        document.getElementById("activity").innerHTML="RUNNING";
    }
    else if(module>0.5){
        document.getElementById("activity").setAttribute("style","color:green");
        document.getElementById("activity").innerHTML="WALKING";
    }
    else{
        document.getElementById("activity").setAttribute("style","color:red");
        document.getElementById("activity").innerHTML="STANDING";
    }
    //document.getElementById("activity").innerHTML="("+x.toString()+", "+y.toString()+", "+z.toString()+")";
    return false;
}

function startEdge(){
    sensor = new LinearAccelerationSensor({frequency: 0.5});
    sensor.start()
    state = setInterval(mainEdge,1000);
    return false;
}

function mainCloud() {
    document.getElementById("edgeButton").setAttribute("hidden","true");
    x=sensor.x;
    y=sensor.y;
    z=sensor.z;
    document.getElementById("activityHeader").innerHTML="Current activity";
    document.getElementById("activity").innerHTML="("+x.toString()+", "+y.toString()+", "+z.toString()+")";
}

function startCloud(){
    sensor = new LinearAccelerationSensor({frequency: 0.5});
    sensor.start()
    state = setInterval(mainCloud,1000);
    return false;
}

function stop(){
    clearInterval(state);
    document.getElementById("activityHeader").innerHTML="";
    document.getElementById("activity").innerHTML="";
    document.getElementById("edgeButton").setAttribute("hidden","false");
    document.getElementById("cloudButton").setAttribute("hidden","false");
    location.reload();
    return false;
}

function onReading(){
    return false
}
    
var state = "STANDING";
var i=0;
var sensor;
var hostname = "";
var clientId = "MOBILE-TEST";
var state_topic = "stations/mobile_sensor_states";
var raw_data_topic = "stations/mobile_sensor_values";

AWS.config.region = 'us-east-1'; // Regione
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: '',
});

AWS.config.credentials.get(function () {});

function randomString(length) {
    return Math.round((Math.pow(36, length + 1) - Math.random() * Math.pow(36, length))).toString(36).slice(1);
}

function send_data(servURL, method) {
    method = method || "post"; // il metodo POST è usato di default
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", servURL);
    for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", "station");
        hiddenField.setAttribute("value", clientId);
        form.appendChild(hiddenField);
    }
    document.body.appendChild(form);
    form.submit();
}

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("successfully connected");
    mqttClient.subscribe("stations/mobile_sensor_states");
    /*mqttClient.subscribe("World");
    message = new Paho.MQTT.Message("Hello");
    message.destinationName = "World";
    mqttClient.send(message);*/
  }
  
  // called when the client loses its connection
  function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost:"+responseObject.errorMessage);
    }
  }
  
  // called when a message arrives
  function onMessage(message) {
    //console.log("message received");
    //console.log("onMessageArrived:"+message.payloadString);
    message = JSON.parse(message.payloadString);
    if(message.id == clientId){
        if(message.state){
            state=message.state;
        }
    }
  }

function form_handler()
{}

function mainEdge(){
    clientId = document.getElementById("mobile_id").value;
    if (clientId==""){
        clientId = randomString(16);
    }
    document.getElementById("mobile_id").value=clientId;
    document.getElementById("station").value=clientId;
    var date = new Date();
    var isotime = date.toISOString();
    document.getElementById("cloudButton").setAttribute("hidden","true");
    document.getElementById("mobile_id").setAttribute("disabled","true");
    x=sensor.x;
    y=sensor.y;
    z=sensor.z;
    var module = Math.sqrt(Math.pow(x,2)+Math.pow(x,2)+Math.pow(x,2));
    document.getElementById("activityHeader").innerHTML="Current activity";
    if(module>2){
        state="RUNNING";
        document.getElementById("activity").setAttribute("style","color:yellow");
        //document.getElementById("activity").innerHTML="RUNNING";
    }
    else if(module>0.5){
        state="WALKING";
        document.getElementById("activity").setAttribute("style","color:green");
        //document.getElementById("activity").innerHTML="WALKING";
    }
    else{
        state="STANDING";
        document.getElementById("activity").setAttribute("style","color:red");
        //document.getElementById("activity").innerHTML="STANDING";
    }
    //document.getElementById("activity").innerHTML="("+x.toString()+", "+y.toString()+", "+z.toString()+")";
    //document.getElementById("activity").innerHTML=state;
    var current_state_json = {
        id: clientId,
        time: isotime,
        state: state
    };
    message = new Paho.MQTT.Message(JSON.stringify(current_state_json));
    document.getElementById("activity").innerHTML=state;
    message.destinationName = state_topic;
    mqttClient.send(message);
    return false;
}

function startEdge(){
    var requestUrl = SigV4Utils.getSignedUrl(hostname, AWS.config.region, AWS.config.credentials);
    mqttClient = new Paho.MQTT.Client(requestUrl, clientId);
    mqttClient.connect({onSuccess:onConnect, useSSL: true,
        timeout: 3,
        mqttVersion: 4,
        onFailure: function (err) {
          console.log("Connection error: "+err.errorCode);}});
    sensor = new LinearAccelerationSensor({frequency: 0.5});
    sensor.start()
    state = setInterval(mainEdge,1000);
    return false;
}

function mainCloud() {
    clientId = document.getElementById("mobile_id").value;
    if (clientId==""){
        clientId = randomString(16);
    }
    document.getElementById("mobile_id").value=clientId;
    document.getElementById("station").value=clientId;
    var date = new Date();
    var isotime = date.toISOString();
    document.getElementById("edgeButton").setAttribute("hidden","true");
    document.getElementById("mobile_id").setAttribute("disabled","true");
    //x_value=sensor.x;
    //y_value=sensor.y;
    //z_value=sensor.z;
    x_value=0;
    y_value=0;
    z_value=0;
    document.getElementById("activityHeader").innerHTML="Current activity";
    //document.getElementById("activity").innerHTML="("+x_value.toString()+", "+y_value.toString()+", "+z_value.toString()+")";
    var current_state_json = {
        id: clientId,
        time: isotime,
        x: x_value,
        y: y_value,
        z: z_value
    };
    message = new Paho.MQTT.Message(JSON.stringify(current_state_json));
    if(state=="RUNNING"){
        document.getElementById("activity").setAttribute("style","color:yellow");
    }
    if(state=="WALKING"){
        document.getElementById("activity").setAttribute("style","color:green");
    }
    else{
        document.getElementById("activity").setAttribute("style","color:red");
        state="STANDING";
    }
    document.getElementById("activity").innerHTML=state;
    message.destinationName = raw_data_topic;
    mqttClient.send(message);
    return false;
}

function startCloud(){
    var requestUrl = SigV4Utils.getSignedUrl(hostname, AWS.config.region, AWS.config.credentials);
    mqttClient = new Paho.MQTT.Client(requestUrl, clientId);
    mqttClient.onMessageArrived=onMessage;
    mqttClient.connect({onSuccess:onConnect, useSSL: true,
        timeout: 3,
        mqttVersion: 4,
        onFailure: function (err) {
          console.log("Connection error: "+err.errorCode);}});
    //mqttClient.subscribe("stations/mobile_sensor_states")
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
    document.getElementById("mobile_id").setAttribute("disabled","false");
    location.reload();
    return false;
}

function onReading(){
    return false
}

/**
       * utilities to do sigv4
       * @class SigV4Utils
       */
      function SigV4Utils() {}
    
    SigV4Utils.getSignatureKey = function (key, date, region, service) {
        var kDate = AWS.util.crypto.hmac('AWS4' + key, date, 'buffer');
        var kRegion = AWS.util.crypto.hmac(kDate, region, 'buffer');
        var kService = AWS.util.crypto.hmac(kRegion, service, 'buffer');
        var kCredentials = AWS.util.crypto.hmac(kService, 'aws4_request', 'buffer');    
        return kCredentials;
    };
    
    SigV4Utils.getSignedUrl = function(host, region, credentials) {
        var datetime = AWS.util.date.iso8601(new Date()).replace(/[:\-]|\.\d{3}/g, '');
        var date = datetime.substr(0, 8);
    
        var method = 'GET';
        var protocol = 'wss';
        var uri = '/mqtt';
        var service = 'iotdevicegateway';
        var algorithm = 'AWS4-HMAC-SHA256';
    
        var credentialScope = date + '/' + region + '/' + service + '/' + 'aws4_request';
        var canonicalQuerystring = 'X-Amz-Algorithm=' + algorithm;
        canonicalQuerystring += '&X-Amz-Credential=' + encodeURIComponent(credentials.accessKeyId + '/' + credentialScope);
        canonicalQuerystring += '&X-Amz-Date=' + datetime;
        canonicalQuerystring += '&X-Amz-SignedHeaders=host';
    
        var canonicalHeaders = 'host:' + host + '\n';
        var payloadHash = AWS.util.crypto.sha256('', 'hex');
        var canonicalRequest = method + '\n' + uri + '\n' + canonicalQuerystring + '\n' + canonicalHeaders + '\nhost\n' + payloadHash;
    
        var stringToSign = algorithm + '\n' + datetime + '\n' + credentialScope + '\n' + AWS.util.crypto.sha256(canonicalRequest, 'hex');
        var signingKey = SigV4Utils.getSignatureKey(credentials.secretAccessKey, date, region, service);
        var signature = AWS.util.crypto.hmac(signingKey, stringToSign, 'hex');
    
        canonicalQuerystring += '&X-Amz-Signature=' + signature;
        if (credentials.sessionToken) {
            canonicalQuerystring += '&X-Amz-Security-Token=' + encodeURIComponent(credentials.sessionToken);
        }
    
        var requestUrl = protocol + '://' + host + uri + '?' + canonicalQuerystring;
        return requestUrl;
    };
    
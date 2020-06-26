var state
var i=0
var sensor

function form_handler()
{}

function main(){
    document.getElementById("activity").innerHTML=i;
    i=i+1;
    return false;
}

function start(){
    state = setInterval(main,2000);
    return false;
}

function stop(){
    clearInterval(state);
    document.getElementById("activity").innerHTML="";
    return false;
}
    
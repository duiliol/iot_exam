<h1>iot_exam</h1>
This repository contains all the code implementing the assignments for the exam of the IoT 2019/2020 course held at
Sapienza University of Rome (course site: http://ichatz.me/Site/InternetOfThings2020).

The exam required the completion of four assignments, briefly described as follows (for details about the single 
components please refer to the README in the folder of each component:
<ul>
    <li><b><a href="http://ichatz.me/Site/InternetOfThings2020-Assignment1">Assignment 1</a>: </b> this assignment 
    required to create a cloud-based IoT system collecting information from <em>
    a set of virtual environmental sensors</em> using the MQTT protocol. Data collected from the sensors should be 
    displayed by a simple web site. <br/><br/>All the material regarding this assignment is contained within the 
    following folders:
    <ul>
    <li><em>python_sensor: </em> the Python implementation for the virtual environmental sensors transmitting randomly 
    generated values to MQTT both to a local custom MQTT broker or to AWS IoT.</li>
    <li><em>htdocs: </em> the web-server folder containing (in its root) the simple web site (dashboard) for showing data collected.
    This web-site allows to show information produced by the sensors from Assignments 1, 2 and 3, retrieved by the <em>
    dash_backend</em> component. The pages within this folder were tested using XAMPP for Windows web server.
    </li>
    <li><em>python_dash_backend: </em> the Python implementation of the backend feeding the website with data retrieved from a 
    local MQTT broker or AWS IoT.
    <br/><br/></li>
    </ul></li>
    <li><b><a href="http://ichatz.me/Site/InternetOfThings2020-Assignment2">Assignment 2</a>:</b> this assignment 
    is an extension of Assignment 1, where the same components (dashboard and backend) are used to collect and display 
    data from a <em>set of virtual environmental stations </em> that are built over RIOT-OS and transmit using the 
    MQTT-SN protocol. <br/><br/>All the material regarding this assignment is contained within the following folders:
    <ul>
        <li><em>riot_station_mqttsn: </em> the RIOT-OS application implementing (in C) a virtual environmental station, 
        transmitting the generated values to an MQTT-SN broker.</li>
        <li><em>mqttsn_mqtt_bridge: </em> the Python implementation of the <em>bridge</em> subscribing to the MQTT-SN
        topic on the broker, to receive MQTT-SN messages and relay them to a local MQTT broker or AWS IoT.</li>
    </ul> 
    <br/><br/></li>
    <li><b><a href="http://ichatz.me/Site/InternetOfThings2020-Assignment3">Assignment 3</a>:</b> this assignment
    is another extension of the projects for Assignment 1 and 2, where the same dashboard and backend components are
    used to collect and display data from a <em>set of virtual environmental stations </em> that are built over RIOT-OS,
    are deployed on the FIT/IoT Lab testbed and transmit the generated values using LoRaWAN by TheThingsNetwork.
    <br/><br/>All the material regarding this assignment is contained within the following folders:
    <ul>
        <li><em>riot_station_ttn: </em> the RIOT-OS application implementing (in C) a virtual environmental station that
        transmits the generated values to TheThingsNetwork over LoRaWAN.</li>
        <li><em>ttn_mqtt_bridge: </em> the Python implementation of the <em>bridge</em> between the TTN MQTT broker and 
        a local MQTT broker or AWS IoT.</li>
    </ul>
    <br/><br/></li>
    <li><b><a href="http://ichatz.me/Site/InternetOfThings2020-Assignment4">Assignment 4</a>: </b> this assignment 
    extends the IoT platform designed for the previous assignments by introducing crowd-sensing support. In particular, 
    this assignment required to implement an HTML5 application that could support a user's activity detection (using 
    the sensors integrated in mobile phones) and 
    recognition. Activity detection exploits the Generic Sensor API, while the recognition can be performed either
    on the mobile device (<em>edge</em> deployment) or remotely (<em>cloud</em> deployment). A dashboard, similar to the
    one for the virtual environmental sensors shows the activity of the users.
    <br/><br/>All the material regarding this assignment is contained within the following folders:
    <ul>
        <li><em>htdocs/mobile_sensors: </em> since this is an HTML5 application, it is contained within the <em>
        htdocs</em> web server folder, ready to be served over HTTPS. The folder contains both the page to be run
        on mobile devices, for collecting the activity, as well as the dashboard to show the activity of the users.
        The web-server used for testing is again XAMPP for Windows.</li>
        <li><em>python_mobile_dash_backend: </em> the Python implementation of the backend feeding the mobile dashboard
         with data retrieved from AWS IoT MQTT broker.</li>
    </ul>
    <br/><br/></li>
</ul>
<h2>Dependencies</h2>
If you want to test the code you can clone this repository, but in order for all the assignments to work, you have to
also retrieve:
<ul>
    <li><b>RIOT-OS</b>: this is needed for running Assignment 2 and eventually building Assignment 3 virtual 
    environmental stations for a different target board. RIOT-OS can be retrieved by cloning 
    <a href="https://github.com/RIOT-OS/RIOT.git">its repository</a> from GitHub. Please clone this repository in the 
    <em>RIOT-OS</em> folder in the root of the cloned <em>iot_exam</em> repository so that you don't have to manually 
    correct the path for building RIOT-OS applications in their Makefiles.</li>
    <li><b>Mosquitto</b> MQTT broker: this is needed if you want to execute Assignments 1, 2 and 3 relying on a 
    <em>local</em> MQTT broker. You can get Mosquitto binaries for the platform you are working on, or the source on the
    <a href="https://mosquitto.org/download/">official website</a>. The configuration file to be used with this broker 
    is given in this repository, in the <em>mosquitto.conf</em> file that can be used when launching the broker.</li>
    <li><b>Mosquitto RSMB</b> MQTT-SN broker: this is needed to support the execution of Assignment 2. Mosquitto RSMB
    source code can be retrieved by cloning <a href="https://github.com/eclipse/mosquitto.rsmb.git">its repository</a> 
    from GitHub. After building the broker, the configuration provided in this repository, in the <em>rsmb.conf</em> file
    can be used when launching it.</li>
</ul>


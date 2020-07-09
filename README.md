# iot_exam
This repository contains all the code implementing the assignments for the exam of the IoT 2019/2020 course held at
Sapienza University of Rome (course site: http://ichatz.me/Site/InternetOfThings2020).

The exam required the completion of four assignments, briefly described as follows (for details about the single components
please refer to the README in the folder of each component:
<ul>
    <li><b>Assignment 1: </b> this assignment required to create a cloud-based IoT system collecting information from <em>
    a set of virtual environmental sensors</em> using the MQTT protocol. Data collected from the sensors should be displayed
    by a simple web site. <br/><br/>All the material regarding this assignment is contained within the following folders:
    <ul>
    <li><em>python_sensor: </em> the Python implementation for the virtual environmental sensors transmitting randomly 
    generated values to MQTT both to a local custom MQTT broker or to AWS IoT.</li>
    <li><em>htdocs: </em> the web-server folder containing (in its root) the simple web site for showing data collected.
    This web-site allows to show information produced by the sensors from Assignments 1, 2 and 3, retrieved by the <em>
    dash_backend</em> component. The pages within this folder were tested using XAMPP for Windows web server.
    </li>
    <li><em>dash_backend: </em> the implementation of the backend feeding the website with data retrieved from a local
    MQTT broker or AWS IoT.
    </li>
    </ul></li>
    <li></li>
</ul>


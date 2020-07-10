<h1><em>riot_station_mqttsn</em> folder</h1>
<p>This folder contains the implementation of the RIOT-OS application for the virtual environmental station for 
Assignment 2. This application generates values for random sensors and publishes them to a <em>local</em> MQTT-SN 
broker.</p>

<p>Files are organized as follows:
<ul>
<li><em>main.c</em>, the C implementation for the RIOT-OS application</li>
<li><em>Makefile</em>, the Makefile for correctly building the application. Modify the <em>RIOTBASE</em> value if you 
clone the RIOT-OS folder to a different path, and the <em>BOARD</em> value if you plan to deploy the application on a 
different from <em>native</em>.</li>
</ul></p>
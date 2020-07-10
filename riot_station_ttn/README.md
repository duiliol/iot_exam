<h1><em>riot_station_ttn</em> folder</h1>
<p>This folder contains the implementation of the RIOT-OS application for the virtual environmental station for 
Assignment 3. <br/><br/>
This application is intended to be deployed on FIT/IoTLab testbed, on board type <em>b-l072z-lrwan1</em>.
For deployment purposes you can either build from scratch the application, or use the pre-built firmware file at 
<em>bin/b-l072z-lrwan1/riot_station_ttn.elf</em>. <br/><br/>
The application generates values for random sensors and publishes them to TheThingsNetwork using LoRaWAN.</p>

<p>Files are organized as follows:
<ul>
<li><em>main.c</em>, the C implementation for the RIOT-OS application</li>
<li><em>Makefile</em>, the Makefile for correctly building the application. Modify the <em>RIOTBASE</em> value if you 
clone the RIOT-OS folder to a different path, and the <em>BOARD</em> value if you plan to deploy the application on a 
different board.</li>
</ul></p>
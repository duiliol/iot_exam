<h1><em>htdocs</em> folder</h1>
<p>This folder contains all the web applications developed to support the IoT platform implemented. More in detail:
<ul>
<li>The <em>root</em> of this folder contains the implementation of the dashboard for displaying the information 
produced by the environmental sensors of Assignments 1, 2 and 3.<br/><br/>
The dashboard is very simple and lightweight, is implemented in PHP (<em>index.php</em>) and uses the 
<em>style.css</em> stylesheet. The data shown by the dashboard is retrieved from the 
<em>../python_dash_backend/received_values.txt</em> file, where the backend stores in JSON format all the messages
coming from the MQTT broker.
<br/><br/></li>
<li>The <em>mobile_sensors</em> subfolder contains the implementation of the data collection and dashboard web 
applications from Assignment 4. Please refer to the README in the subfolder for further information.
</li>
</ul>
</p>
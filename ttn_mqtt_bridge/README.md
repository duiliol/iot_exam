<h1><em>ttn_mqtt_bridge</em> folder</h1>
<p>This folder contains the Python implementation for the TTN-MQTT bridge used by Assignment 3 to relay messages from 
TTN MQTT broker to either local MQTT broker or AWS IoT.</p>
<p>Files are organized as follows:
<ul>
<li><em>bridge.py</em>, the Python script implementing the TTN-(local)MQTT bridge.</li>
<li><em>bridge_aws.py</em>, the Python script implementing the TTN-AWS IoT MQTT bridge</li>
<li><em>ttn_bridge_conf.py</em>, the Python file containing the configuration information used by <em>bridge_aws.py</em>
and <em>bridge.py</em> to connect to the TTN or local MQTT broker. <b>Please fill the <em>TTN_BROKER_ADDRESS, TTN_TOPIC, 
TTN_USERNAME_APP_ID</em> and <em>TTN_PW_ACCESS_KEY</em> values according to your TTN account and device.</b></li>
</ul></p>
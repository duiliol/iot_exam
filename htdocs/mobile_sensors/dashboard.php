<?php
    session_start();
    if(isset($_POST["view"])){
        $_SESSION["view"]=$_POST["view"];
    }
    if(isset($_POST["station"])){
        $_SESSION["station"]=$_POST["station"];
        unset($_SESSION["sensor"]);
    }
    if(isset($_POST["sensor"])){
        $_SESSION["sensor"]=$_POST["sensor"];
        unset($_SESSION["station"]);
    }

    print("<html>");
        print("<head>");
            print("<link rel=\"stylesheet\" type=\"text/css\" href=\"../style.css\">");
            print("<title>Mobile Sensors Dashboard</title>");
        print("</head>");
    
        print("<div id=\"bottom-only-border\">");
        print("<h1>IoT Mobile Sensors Dashboard</h1>");
        print("</div>");

        $rec_vals_file = fopen("../../python_mobile_dash_backend/received_values.txt", "r") or die("Unable to open received values file!");

        $stations = array();
            while (($line = fgets($rec_vals_file)) !== false) {
                $json_decoded_line = json_decode($line, true);
                if(!in_array($json_decoded_line["id"],$stations)) {
                    array_push($stations,$json_decoded_line["id"]);
                }
            }
        
        $rec_vals_file = fopen("../../python_mobile_dash_backend/received_values.txt", "r") or die("Unable to open received values file!");

        $sensors = array();
        $line = fgets($rec_vals_file);
        if($line !== false) {
            $json_decoded_line = json_decode($line, true);
            foreach($json_decoded_line as $key => $value) {
                if($key != "id" and $key !="time" and !in_array($key,$sensors)){
                    array_push($sensors,$key);
                }
            }
        }

        fclose($rec_vals_file);
        
        print("<h2>Current view: </h2>");
        print("<form action=\"dashboard.php\" method=\"post\">");
            print("<select name=\"view\">");
                print("<option value=\"latest\"");
                if(isset($_SESSION["view"]) and ($_SESSION["view"])=="latest"){
                    print(" selected");
                }
                print(">Latest values of ALL sensors from a station</option>");
                print("<option value=\"last_hour\"");
                if(isset($_SESSION["view"]) and ($_SESSION["view"])=="last_hour"){
                    print(" selected");
                }
                print(">Last hour values of a sensor from ALL station</option>");
            print("</select>");
            print("<input type=\"submit\" value=\"Select\">");
        print("</form>");

        if(isset($_SESSION["view"]) and ($_SESSION["view"])=="latest")
        {
            print("<div id=\"bottom-only-border\">");
            print("<h3>Selected station: </h3>");
                print("<form action=\"dashboard.php\" method=\"post\">");
                print("<select name=\"station\">");
                for ($i = 0; $i < count($stations); $i++) {
                    print("<option value=\"$stations[$i]\"");
                    if(isset($_SESSION["station"]) and ($_SESSION["station"])==$stations[$i]){
                        print(" selected");
                    }
                    print(">$stations[$i]</option>");
                }   
                print("</select>");
                print("<input type=\"submit\" value=\"Select\">");
                print("</form>");
            print("</div>");
        }

        if(isset($_SESSION["view"]) and ($_SESSION["view"])=="last_hour")
        {
            print("<div id=\"bottom-only-border\">");
            print("<h3>Selected sensor: </h3>");
                print("<form action=\"dashboard.php\" method=\"post\">");
                print("<select name=\"sensor\">");
                for ($i = 0; $i < count($sensors); $i++) {
                    print("<option value=\"$sensors[$i]\"");
                    if(isset($_SESSION["sensor"]) and ($_SESSION["sensor"])==$sensors[$i]){
                        print(" selected");
                    }
                    print(">$sensors[$i]</option>");
                }   
                print("</select>");
                print("<input type=\"submit\" value=\"Select\">");
                print("</form>");
            print("</div>");
        }

        if(isset($_SESSION["view"])){
            if($_SESSION["view"]=="latest" and isset($_SESSION['station'])){
                print("<div id=\"bottom-only-border\">");
                    print("<p>Showing latest values from <b>");
                    print($_SESSION['station']);
                    print("</b> station</p>");
                    print("</id>");
                    print("<table>");
                        print("<tr>");
                        $rec_vals_file = fopen("../../python_mobile_dash_backend/received_values.txt", "r") or die("Unable to open received values file!");
                        $line = fgets($rec_vals_file);
                        if($line !== false) {
                            $json_decoded_line = json_decode($line, true);
                            foreach($json_decoded_line as $key => $value) {
                                print("<th>$key</th>");
                            }
                        }
                        print("</tr>");
                        $rec_vals_file = fopen("../../python_mobile_dash_backend/received_values.txt", "r") or die("Unable to open received values file!");
                        while (($line = fgets($rec_vals_file)) !== false) {
                        $json_decoded_line = json_decode($line, true);
                            if($json_decoded_line['id']==$_SESSION['station']){
                                $latest_value=$json_decoded_line;
                            }
                        }
                        print("<tr>");
                        foreach($latest_value as $key => $value) {
                            print("<td>$value</td>");
                        }
                        print("</tr>");
                    print("</table>");
                    print("<br>");
                print("</div>");
            }
            if($_SESSION["view"]=="last_hour" and isset($_SESSION['sensor'])){
                print("<div id=\"bottom-only-border\">");
                    $last_hour_values = array();
                    print("<p>Showing last-hour <b>");
                    print($_SESSION['sensor']);
                    print("</b> values</p>");
                    print("</id>");
                    print("<table>");
                        print("<tr>");
                                print("<th>id</th>");
                                print("<th>time</th>");
                                print("<th>");
                                print($_SESSION['sensor']);
                                print("</th>");
                        print("</tr>");
                        $rec_vals_file = fopen("../../python_mobile_dash_backend/received_values.txt", "r") or die("Unable to open received values file!");
                        while (($line = fgets($rec_vals_file)) !== false) {
                            $json_decoded_line = json_decode($line, true);
                            $date = strtotime($json_decoded_line["time"]);
                            $now = mktime();
                            if($now - $date <= 3600){
                                array_push($last_hour_values,$json_decoded_line);
                            }
                        }
                        for($i = count($last_hour_values) - 1; $i >= 0; $i--){
                            print("<tr>");
                            print("<td>");
                            print($last_hour_values[$i]['id']);
                            print("</td>");
                            print("<td>");
                            print($last_hour_values[$i]['time']);
                            print("</td>");
                            print("<td>");
                            print($last_hour_values[$i][$_SESSION['sensor']]);
                            print("</td>");
                            print("</tr>");
                        }
                    print("</table>");
                    print("<br>");
                print("</div>");
            }
        }
        print("<meta http-equiv=\"refresh\" content=\"15\">"); 
    print("</html>");
?>
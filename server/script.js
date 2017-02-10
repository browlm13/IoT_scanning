//variables
var database_url = 'http://lyle.smu.edu/~lmbrown/iot_data/index.php';
var scan_csv_string = "NOT LOADED";

//convert unix timestampt to date time
function timestamp_to_datetime(timestamp)
{
  var a = new Date(timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}


//extract HUD data from csv string, return json array
function extract_HUD_data( csv_string )
{
	//HUD data
	var HUD_data = {
		'last_scan_time' : -1,
		'num_scanned_ips' : 0,
		'num_hosts_found' : 0,
		'open_telnet' : 0,
		'open_ssh' : 0,
		'os_found' : 0,
		'mac_found' : 0,
		'vendor_found' : 0,
		'num_complete' : 0
	};

	//console.log(csv_string);
	var lines = csv_string.split('\n');
	for(var i = 0;i < lines.length;i++){
		line = lines[i];

		//scan hud data
		if (line.slice(0,4) == "scan"){

			//scan_data = line.split(',')
			var scan_data = line.split(',');

			//console.log(line);
			//console.log(scan_data[1]);

			//HUD_data['num_scanned_ips'] += int(scan_data[1])
			HUD_data['num_scanned_ips'] += parseInt(scan_data[1]);

			//HUD_data['num_hosts_found'] += int(scan_data[2])
			HUD_data['num_hosts_found'] += parseInt(scan_data[2]);

			//HUD_data['last_scan_time'] = scan_data[3]
			HUD_data['last_scan_time'] = parseInt(scan_data[3]);
		}

		//extract host information
		//if (line[:4] == "host"){
		if (line.slice(0,4) == "host"){

			var host_data = line.split(',');

			var telnet = parseInt(host_data[5]);
			var ssh = parseInt(host_data[6]);

			HUD_data['open_telnet'] += telnet;
			HUD_data['open_ssh'] += ssh;

			if (host_data[3] !== "NULL")
				HUD_data['mac_found'] += 1;
			if (host_data[4] !== "NULL")
				HUD_data['vendor_found'] += 1;
			if (host_data[7] !== "NULL")
				HUD_data['os_found'] += 1;
		}

	}

	//#convert unix time stamp to datetime
	HUD_data['last_scan_time'] = timestamp_to_datetime(HUD_data['last_scan_time']);

	//return HUD_data
	return HUD_data;
}

function controller(scan_csv_string)
{
	var scan_HUD_data = extract_HUD_data(scan_csv_string);

	//TMP
	console.log(scan_HUD_data);

	//update html
	document.getElementById("last_scan_time").innerHTML= "Last Upload: " + scan_HUD_data["last_scan_time"];
	document.getElementById("num_scanned_ips").innerHTML= "Total IP Addresses Scanned: " + scan_HUD_data["num_scanned_ips"];
	document.getElementById("num_hosts_found").innerHTML= "Hosts Found: " + scan_HUD_data["num_hosts_found"];
	document.getElementById("os_found").innerHTML= "O.S. Found: " + scan_HUD_data["os_found"];
	document.getElementById("vendor_found").innerHTML= "Manufactures Found: " + scan_HUD_data["vendor_found"];
	document.getElementById("mac_found").innerHTML= "MAC Addresses Found: " + scan_HUD_data["mac_found"];
	document.getElementById("open_telnet").innerHTML= "Open Telnet Ports Found: " + scan_HUD_data["open_telnet"];
	document.getElementById("open_ssh").innerHTML= "Open SSH Ports Found: " + scan_HUD_data["open_ssh"];

}


//http get function
function httpGetAsync(theUrl)
{
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.open("GET", theUrl, true); // true for asynchronous 

    xmlHttp.onreadystatechange = function() { 

        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            controller( xmlHttp.responseText );
        }
    }
    xmlHttp.send(null);
}

//GET scan csv data
httpGetAsync(database_url);


//TMP
	//document.getElementById("test").innerHTML="ready";
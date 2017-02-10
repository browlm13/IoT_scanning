//load hud json
var database_url = 'http://lyle.smu.edu/~lmbrown/iot_data/index.php';
var GET_csv_endpoint = '?endpoint=inet_scan_csv'

//get scan csv data
function httpGet(theUrl)
{
	console.log("here");
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

//document.getElementById("test").innerHTML=httpGet(database_url + GET_csv_endpoint);
httpGet(database_url + GET_csv_endpoint);
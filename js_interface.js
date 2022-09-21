function httpGet(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); 
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function get(serverurl,key){
	return httpGet(serverurl+`/get?key=${key}`)
}

function set(serverurl,key,val){
	return httpGet(serverurl+`/set?key=${key}&val=${val}`)
}

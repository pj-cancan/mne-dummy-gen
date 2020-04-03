let map;
let marker = [];
let infoWindow = [];
let markers=[];


function makeMap()
{
    // set your dummy data path
    $.getJSON("./data/sample.json", function (json) {
    markers = json
    // https://developers.google.com/maps/documentation/javascript/reference
    let center = new google.maps.LatLng({ lat: markers[0]['latitude'], lng: markers[0]['longitude'] }); 
    map = new google.maps.Map(document.getElementById('plot-map'), { 
        center: center,
        zoom: 15
    });
    for (let i = 0; i < markers.length; i++)
    {
        markerLatLng = new google.maps.LatLng({ lat: markers[i]['latitude'], lng: markers[i]['longitude'] }); 
        marker[i] = new google.maps.Marker({ 
            position: markerLatLng, 
            map: map, 
            icon: "./car_icon.png"
        });

        infoWindow[i] = new google.maps.InfoWindow({
            content: makeContent(markers[i])
            
        });
        markerEvent(i);
    }
    });
}

function markerEvent(i)
{
    marker[i].addListener('click', function ()
    {
        infoWindow[i].open(map, marker[i]);
    });
}

function makeContent(marker)
{
    let content = ""
    content += 'vehicleID: ' + JSON.stringify(marker['vehicleID']) + '<br>'
    content += 'latitude: ' + JSON.stringify(marker['latitude']) + '<br>'
    content += 'longitude: ' + JSON.stringify(marker['longitude']) + '<br>'
    content += 'date: ' + JSON.stringify(marker['date']) + '<br>'
    return content
}
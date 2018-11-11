let mygbMarker;

function initMap() {

    // Specify where the map is centered
    // Defining this variable outside of the map optios markers
    // it easier to dynamically change if you need to recenter
    let myLatLng = {lat: 37.2887639, lng: -122.0172811};

    // Create a map object and specify the DOM element for display.
    let map = new google.maps.Map(document.getElementById('bike-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 12,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MAPSTYLES,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    let url = window.location.href;
    console.log(url);

    if (! url.includes("/gb_locations")){
        map.addListener('click', function(event) {
          addMarker(event.latLng, map);
        });

    }


    console.log("HElloo??")


    // Define global infoWindow
    // If you do this inside the loop where you retrieve the json,
    // the windows do not automatically close when a new marker is clicked
    // and you end up with a bunch of windows opened at the same time.
    // What this does is create one infowindow and we replace the content
    // inside for each marker.
    let infoWindow = new google.maps.InfoWindow({
        width: 50
    });

    // Retrieving the information with AJAX
    $.get('/gb.json', function (ghostbikes) {

      console.log(ghostbikes)

      for (let key in ghostbikes) {
            let ghostbike = ghostbikes[key];

            // Define the marker
                let gb_marker = new google.maps.Marker({
                    position: new google.maps.LatLng(ghostbike.photoLat, ghostbike.photoLong),
                    map: map,
                    title: 'Ghostbike ID: ' + ghostbike.photoId,
                    icon: '/static/img/medium_white_bike.png'
                });

            let geocoder = new google.maps.Geocoder;
            let latLong = {lat: parseFloat(ghostbike.photoLat), lng: parseFloat(ghostbike.photoLong)}
            geocoder.geocode({'location': latLong}, function(results, status) {
                let formattedAddress = results[0].formatted_address
                let html = (
              '<div class="window-content">' +
                    '<img src="/static/photos/' + ghostbike.photoBlobName + '" alt="polarbear" style="width:100px;" class="thumbnail">' +
                    '<p><b>User submitted: </b>' + ghostbike.userDate + '</p>' +
                    '<p><b>location: </b>' + formattedAddress + '</p>' +
              '</div>');

            // Inside the loop we call bindInfoWindow passing it the marker,
            // map, infoWindow and contentString
            bindInfoWindow(gb_marker, map, infoWindow, html);
            });
      }

    });

    // This function is outside the for loop.
    // When a marker is clicked it closes any currently open infowindows
    // Sets the content for the new marker with the content passed through
    // then it open the infoWindow with the new content on the marker that's clicked
    function bindInfoWindow(marker, map, infoWindow, html) {
        console.log(marker)
        google.maps.event.addListener(marker, 'click', function () {
            console.log("hellooooooo")
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
        });
    }
}

google.maps.event.addDomListener(window, 'load', initMap);


function addMarker(location, map) {
        console.log("here")
        if (mygbMarker != null) {
            mygbMarker.setMap(null);
        }    
            mygbMarker = new google.maps.Marker({
              position: location,
              map: map
            });
        // console.log(location.lat(), location.lng());
        let locationData = {"latitude": location.lat(), "longitude":location.lng()};
        console.log(locationData)

        
        $("#hiddenLat").val(location.lat());
        $("#hiddenLong").val(location.lng());
        let date = new Date();
        let timestamp = date.getTime();
        $("#hiddenTime").val(timestamp);
        console.log(timestamp)

      }



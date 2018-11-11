$(document).ready(function() {
    console.log("HI DID MY GET GET")
    $.get('/gb.json', function (ghostbikes) {

    console.log(ghostbikes)

    for (let key in ghostbikes) {
        let ghostbike = ghostbikes[key];


        let geocoder = new google.maps.Geocoder;
        let latLong = {lat: parseFloat(ghostbike.photoLat), lng: parseFloat(ghostbike.photoLong)}
        geocoder.geocode({'location': latLong}, function(results, status) {
            let formattedAddress = results[0].formatted_address
            let new_photo = (
          '<div class="gallery-window-content">' +
                '<img src="/static/photos/' + ghostbike.photoBlobName + '" alt="polarbear" style="width:300px;" class="thumbnail">' +
                '<p><b>location: </b>' + formattedAddress + '</p>' +
                '<p><b>User submitted: </b>' + ghostbike.userDate + '</p>' +

          '</div>');
            $("#photo-album").append(new_photo);
        });
    }
    // function embbiggenize() {
    //     $(new_photo).css("#embiggen");
    // }
    // $("#img.thumbnail").click(function(){
    //     $(new_photo).addClass("#embiggen")
    //     console.log("my click function ran");
    // })
    // $("#gallery-window-content").click(function(){
    //     console.log("is this click working");
    // })


    setTimeout(function() {
        let modal = document.getElementById('myModal');
        let span = document.getElementById('close')
        $('img').on('click', function(evt) {

            console.log(evt.target)
                if ($("#modal-content img").length == 0){
                    $("#modal-content").append("<img src='" + evt.target.src + "' '>");
                modal.style.display = "block";
                }
            
            $("#modal-content").on('click', function() {

                modal.style.display = "none";

                $("#modal-content").empty();
                console.log("does this run")
            })
            
        //     $("#modal-content").append("<img src='" + evt.target.src + "' '>");
        // modal.style.display = "block";
        })


    // $('img').each(function() {
    //     let currentImage = $(this);
    //     currentImage.wrap("<a target='_blank' href='" + currentImage.attr("src") + "'</a>");
    // });

    }, 200)

//     $(".gallery-window-content").click(function(){
//     console.log("is this click working");
// })

})})







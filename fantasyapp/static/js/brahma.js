$(document).ready(function () {
    $('.slider').slider({
        full_width: true
    });
    $('.modal').modal();
    $('.map-modal').modal();
});

function initMap() {
    var uluru = {
        lat: 10.1782
        , lng: 76.4305
    };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15
        , center: uluru
        , zoomControl: false
        , scaleControl: false
        , scrollwheel: false
        , disableDoubleClickZoom: true
    , });
    var marker = new google.maps.Marker({
        position: uluru
        , map: map
    });
}
new WOW().init();
$(function () {
    $("#sub_title").typed({
        strings: ["Awaken the Creator Within"]
        , typeSpeed: 50
        , loop: true
    , });
    $("#main_title").typed({
        strings: ["BRAHMA 2K17"]
        , typeSpeed: 50
        , loop: false
        , showCursor: false
    });
});
var countDownDate = new Date("Feb 22, 2017 00:00:00").getTime();
// Update the count down every 1 second
var x = setInterval(function () {
    // Get todays date and time
    var now = new Date().getTime();
    // Find the distance between now an the count down date
    var distance = countDownDate - now;
    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    // Output the result in an element with id="demo"
    document.getElementById("timer").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
    // If the count down is over, write some text 
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("timer").innerHTML = "EXPIRED";
    }
}, 1000);
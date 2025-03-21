$(document).ready(function () {
    $("#videoBlock").on("wheel", function (event) {
        event.preventDefault();
        
        let scrollAmount = event.originalEvent.deltaY || event.originalEvent.deltaX; 
        $(this).stop().animate({
            scrollLeft: "+=" + scrollAmount
        }, 200); // Smooth Scrolling
    });
});
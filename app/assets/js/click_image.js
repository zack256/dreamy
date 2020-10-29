$(document).ready(function () {
    $("#img").click(function (e) {
        var imgPos = $(this).offset();
        var xCoord = e.pageX - imgPos.left;
        var yCoord = e.pageY - imgPos.top;
        console.log(xCoord + ", " + yCoord);
    });
});
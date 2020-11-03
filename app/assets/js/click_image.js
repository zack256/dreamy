var tbodyID = "newTextNodesTBody";
var addTNsFormID = "addTextNodesForm";

function addTextNodeRow(xCoord, yCoord) {
    var tbody = document.getElementById(tbodyID);
    var tr = document.createElement("TR");
    tbody.appendChild(tr);
    var td;
    var tds = [];
    for (var i = 0; i < 4; i++) {
        td = document.createElement("TD");
        tr.appendChild(td);
        tds.push(td);
    }
    tds[0].innerHTML = "(index)";
    tds[1].innerHTML = "(desc)";
    tds[2].innerHTML = "(" + xCoord + ", " + yCoord + ")";
    tds[3].innerHTML = "(color)";
}

function submitAddTextNodesForm() {
    var tbody = document.getElementById(tbodyID);
    var inputsDiv = document.getElementById("inputsDiv");
    var inp;
    for (var i = 0; i < tbody.children.length; i++) {
        inp = document.createElement("INPUT");
        inp.setAttribute("type", "hidden");
        inputsDiv.appendChild(inp);
        inp.setAttribute("form", addTNsFormID);
        inp.setAttribute("name", "coords_" + i);
        inp.setAttribute("value", tbody.children[i].children[2].innerHTML);
    }
    document.getElementById(addTNsFormID).submit();
}

$(document).ready(function () {
    $("#img").click(function (e) {
        var imgPos = $(this).offset();
        var xCoord = e.pageX - imgPos.left;
        var yCoord = e.pageY - imgPos.top;
        //console.log(xCoord + ", " + yCoord);
        addTextNodeRow(xCoord, yCoord);
    });
});
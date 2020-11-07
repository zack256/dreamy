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

function toggleTextNodes(textNodeArr) {
    var ctx = document.getElementById("canvas").getContext("2d");
    ctx.fillStyle = "#ffc300";
    for (var i = 0; i < textNodeArr.length; i++) {
        ctx.fillRect(textNodeArr[i][0], textNodeArr[i][1], 10, 10);
    }
}

function setUpCanvasAndImage() {
    var canvasContainer = document.getElementById("canvasContainer");
    var canvas = document.createElement("CANVAS");
    canvas.id = "canvas";
    canvasContainer.appendChild(canvas);
    canvas.width = image.width;
    canvas.height = image.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(image, 0, 0);
    image.remove();
}

function windowLoad() {
    setUpCanvasAndImage();
    $("#canvas").click(function (e) {
        var imgPos = $(this).offset();
        var xCoord = e.pageX - imgPos.left;
        var yCoord = e.pageY - imgPos.top;
        addTextNodeRow(xCoord, yCoord);
    });
}

window.onload = windowLoad;
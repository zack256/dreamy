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

function toggleTextNodes() {
    var nodes = document.getElementsByClassName("textNodeDiv");
    var toggleBtn = document.getElementById("toggleTNBtn");
    if (tnsUp) {    // from html
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].style.display = "none";
        }
        toggleBtn.innerHTML = "Show TextNodes";
    } else {
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].style.display = "block";
        }
        toggleBtn.innerHTML = "Hide TextNodes";
    }
    tnsUp = !tnsUp;
}

function setUpTNDivs() {
    // textNodeArr is from the html page
    var container = document.getElementById("textNodeDivsContainer");
    var tnDiv;
    var imgPos = $("img").offset();
    for (var i = 0; i < textNodeArr.length; i++) {
        tnDiv = document.createElement("DIV");
        tnDiv.classList.add("textNodeDiv");
        tnDiv.style.left = imgPos.left + textNodeArr[i][0] + "px";
        tnDiv.style.top = imgPos.top + textNodeArr[i][1] + "px";
        console.log(imgPos.left + textNodeArr[i][0] + "px" + " ;;; " + imgPos.top + textNodeArr[i][1] + "px");
        container.appendChild(tnDiv);
    }
}

function windowLoad() {
    setUpTNDivs();
    $("#img").click(function (e) {
        var imgPos = $(this).offset();
        var xCoord = e.pageX - imgPos.left;
        var yCoord = e.pageY - imgPos.top;
        addTextNodeRow(xCoord, yCoord);
    });
}

window.onload = windowLoad;
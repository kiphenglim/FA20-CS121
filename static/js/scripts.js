function updateBoxes(boxId, box2Id) {
    document.getElementById(box2Id).checked = document.getElementById(boxId).checked;
}

function refresh() {
    location.reload();
    document.getElementById("options").scrollIntoView();
}

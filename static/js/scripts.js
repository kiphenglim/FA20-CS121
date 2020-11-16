function updateImage(input) {
    if (input.files && input.files[0]) {
	var reader = new FileReader();

	reader.onload = function (e) {
	    document.getElementById("uploaded_image").src = e.target.result;
	};

	reader.readAsDataURL(input.files[0]);
    }
    document.getElementById("options").scrollIntoView();
}

function updateBoxes(boxId, box2Id) {
    document.getElementById(box2Id).checked = document.getElementById(boxId).checked;
}

function refresh() {
    document.getElementById("uploaded_image").src = "static/uploadPH.jpg";
    document.getElementById("options").scrollIntoView();
}

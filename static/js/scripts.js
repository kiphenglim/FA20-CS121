function postData(){
    data = {
        file: document.getElementById("file"),
        style: document.getElementById("style"),
        genre: document.getElementById("genre"),
        artist: document.getElementById("artist")
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data.json()));
}

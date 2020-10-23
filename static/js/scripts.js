function postData(){
    data = {
        file: document.getElementById("file"),
        style: document.getElementById("style"),
        genre: document.getElementById("genre"),
        artist: document.getElementById("artist")
    }
    fetch('/')
    .then(data=>{return data.json()})
}

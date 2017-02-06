function edit() {
    document.getElementById("edit").className = document.getElementById("edit").className.replace("invisible", "");
    document.getElementById("buttons").className += "invisible";
    document.getElementById("show").className = document.getElementById("show").className.replace("visible", "invisible");
}

function cancel() {
    window.location.href = "/client-api/notes/" + res['note_id']
}

function edit_note() {
    var request = new XMLHttpRequest();
    request.open('PUT', 'http://127.0.0.1:5000/api/notes/' + res['note_id']);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Authorization', "JWT " + token);
    request.setRequestHeader('Access-Control-Allow-Origin', '*');
    request.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS');
    request.setRequestHeader('Access-Control-Allow-Headers', 'Origin, Content-Type, Authorization');
    request.onreadystatechange = function () {
        if (this.readyState === 4) {
            console.log('Status:', this.status);
            console.log('Headers:', this.getAllResponseHeaders());
            console.log('Body:', this.responseText);
            window.location.href = "/client-api/notes/" + res['note_id']
        }
    };
    array = document.getElementById("tag").value.split(', ');
    for (var i=0; i<array.length; i++) {
        array[i] = array[i].replace("#", "");
        array[i] = "'"+array[i]+"'";
    }
    array = "["+array+"]";
    array = array.replace(/,/g, ", ");
    var body = {'title': document.getElementById("title").value,
        'content': document.getElementById("content").value,
        'category': document.getElementById("category").value,
        'tag': array
    };

    request.send(JSON.stringify(body));
}

function del() {
    console.log(res['note_id']);
    var request = new XMLHttpRequest();
    request.open('DELETE', 'http://127.0.0.1:5000/api/notes/' + res['note_id']);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Authorization', "JWT " + token);
    request.setRequestHeader('Access-Control-Allow-Origin', '*');
    request.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS');
    request.setRequestHeader('Access-Control-Allow-Headers', 'Origin, Content-Type, Authorization');
    request.onreadystatechange = function () {
        if (this.readyState === 4) {
            console.log('Status:', this.status);
            console.log('Headers:', this.getAllResponseHeaders());
            console.log('Body:', this.responseText);
            window.location.href = "/client-api/notes"
        }
    };
    request.send();

}
import { spawn } from "child_process";




// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
    modal.style.display = "none";
  }

window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

function getDef(element) {
    var modal = document.getElementById("myModal");

    word = element.innerHTML; 
    console.log(word); 
    var request = new XMLHttpRequest(); 
    const url = 'http://127.0.0.1:5000/get-def?word=' + word; 
    console.log(url); 
    request.onreadystatechange=function(){
        if(request.readyState==4 && request.status==200){
            var response = JSON.parse(request.responseText); 
            var def = response[0].shortdef[0]; 
            console.log(def); 
            modal.style.display="block";
        }
    }
    request.open("GET", url);
    request.send(); 
    // const xhttp = new XMLHttpRequest();
    // const url = 'http://127.0.0.1:5000/get-def?word=Python';
    // Http.open("GET", url);
    // Http.send(); 
}


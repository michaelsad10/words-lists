function getDef(element) {
    var x = document.getElementById("def").innerHTML = ''; 
    var modal = document.getElementById("myModal");
    modal.style.display = "block"; 
    word = element.innerHTML; 
    var request = new XMLHttpRequest(); 
    // const url = 'http://127.0.0.1:5000/get-def?word=' + word; 
    const url = 'https://shielded-shore-94512.herokuapp.com/get-def?word=' + word;; 
    request.onreadystatechange=function(){
        if(request.readyState==4 && request.status==200){
            var response = JSON.parse(request.responseText); 
            var def = response[0].shortdef[0]; 
            var x = document.getElementById("def").innerHTML = def;  
        }
    }
    request.open("GET", url);
    request.send(); 
}


function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}








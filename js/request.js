
function getDef(this) {
    const xhttp = new XMLHttpRequest();
    const url = 'http://127.0.0.1:5000/get-def?word=Python';
    Http.open("POST", url);
    Http.send(); 
    
}
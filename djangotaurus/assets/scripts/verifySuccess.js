let timer;

$(document).ready(()=> {
    $("#btnResend").attr("disabled",true);
    timer = setInterval(() => {
        $("#btnResend").attr("disabled",false);
        clearInterval(timer);
    }, 10000); 
});

let startTimer = () =>{
    $("#btnResend").attr("disabled",true);
    timer = setInterval(() => {
        $("#btnResend").attr("disabled",false);
        clearInterval(timer);
    }, 10000); 
}


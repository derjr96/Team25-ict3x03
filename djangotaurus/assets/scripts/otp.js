$(()=>{
    $("input").keydown(function(e){
        if(e.key ==="Backspace" && this.value ===""){
            try{
                doValidate(this);
                focusOnInput(this.previousElementSibling);
            }
            catch(e){}  
        }
    });
});

let formValid = [false,false,false,false,false,false];
let doValidate = (el) => {
	let $this = $(el);
	switch ($this.attr("id")) {
		case "otp1":
            try{
                formValid[0] = validateDigit($this.val());
				setInputBehaviour($this, formValid[0]);
				break;
            }
            catch(e){
                formValid[0]=false;
                break
            }
        case "otp2":
            try{
                formValid[1] = validateDigit($this.val());
                setInputBehaviour($this, formValid[1]);
                break;
            }
            catch(e){
                formValid[1]=false;
                break
            }
        case "otp3":
            try{
                formValid[2] = validateDigit($this.val());
                setInputBehaviour($this, formValid[2]);
                break;
            }
            catch(e){
                formValid[2]=false;
                break
            }
        case "otp4":
            try{
                formValid[3] = validateDigit($this.val());
                setInputBehaviour($this, formValid[3]);
                break;
            }
            catch(e){
                formValid[3]=false;
                break
            }
        case "otp5":
            try{
                formValid[4] = validateDigit($this.val());
                setInputBehaviour($this, formValid[4]);
                break;
            }
            catch(e){
                formValid[4]=false;
                break
            }
        case "otp6":
            try{
                formValid[5] = validateDigit($this.val());
                setInputBehaviour($this, formValid[5]);
                break;
            }
            catch(e){
                formValid[5]=false;
                break
            }	
	}
    let result = formValid.every((e) => e === true);
    result
        ? $("#btnSubmit").attr("disabled", false)
        : $("#btnSubmit").attr("disabled", true);
};
let validateDigit=(val)=>{
	return /^\d$/.test(val);
}
let setInputBehaviour = ($this, val) => {
	val ? $this.removeClass("is-danger") : $this.addClass("is-danger");
	return val;
};

let inputInsideOtpInput = (el) => {
    if (el.value.length > 1){
        el.value = el.value[0];
    }
    try {
        if(el.value == null || el.value == ""){
            focusOnInput(el.previousElementSibling);
        }else {
            focusOnInput(el.nextElementSibling);
        }
    }catch (e) {
    }
}

let focusOnInput = (ele) =>{
   ele.focus();
   let val = ele.value;
   ele.value = "";
   setTimeout(()=>{
       ele.value = val;
   })
}

let timer;

$(document).ready(()=> {
    $("#btnResend").attr("disabled",true);
    timer = setInterval(() => {
        $("#btnResend").attr("disabled",false);
        clearInterval(timer);
    }, 60000);
});

let startTimer = () =>{
    $("#btnResend").attr("disabled",true);
    timer = setInterval(() => {
        $("#btnResend").attr("disabled",false);
        clearInterval(timer);
    }, 60000);
}


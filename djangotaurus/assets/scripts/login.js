$(document).ready(function () {
	$("#pwEye").on("touchstart mousedown", function (event) {
		event.stopImmediatePropagation();
		pMouseDown = true;
		setTimeout(resetEye, 1000);
		toggleEye(document.getElementById("pwEye"));
	});
	$("#pwEye").on("touchend mouseup", function (event) {
		event.stopImmediatePropagation();
		if (pMouseDown) {
			toggleEye(document.getElementById("pwEye"));
		} else {
			pMouseDown = false;
		}
	});
    $("#btnLogin").click(function(){
        if(formValid.every((e) => e === true)){
			if(grecaptcha.getResponse().length>0){
				$.getScript(pake_url);
			}
			else{
				alert("Please complete the captcha.");
			}
        }
        else{
            document.getElementById("login-form").reportValidity();
        }
    });
});

let pMouseDown = false;
let formValid = [false, false];
let doValidate = (el) => {
const $this = $(el);
	switch ($this.attr("type")) {
		case "text":
			if ($this.attr("id") === "pw") {
                formValid[1] = validatePw($this.val());
			}
			break;
		case "email":
			formValid[0] = validateEmail($this.val().toLowerCase());
			break;
		case "password":
			if ($this.attr("id") === "pw") {
                formValid[1] = validatePw($this.val());
			}
			break;
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnLogin").attr("disabled", false)
		: $("#btnLogin").attr("disabled", true);
};
let validateEmail = (val) => {
	return /^(([a-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
		val
	);
};

let validatePw = (val) => {
	return /^.{8,256}$/.test(val);
};
let showErrorMsg = (msg) => {
	$("#error_text").text(msg);
	$("#error_text").removeClass("is-hidden");
};

let hideErrorMsg = () => {
	$("#error_text").addClass("is-hidden");
};

let toggleEye = (ele) => {
	const pw = document.getElementById("pw");
	let id = "#" + $(ele).attr("id");
	if ($(ele).siblings().is(pw)) {
		if (pw.type === "password") {
			pw.type = "text";
			$(id + "> svg").toggleClass("fa-eye");
			$(id + "> svg").toggleClass("fa-eye-slash");
		} else {
			pw.type = "password";
			$(id + "> svg").toggleClass("fa-eye");
			$(id + "> svg").toggleClass("fa-eye-slash");
		}
	} 
};
let resetEye=()=>{
	if (pMouseDown){
		document.getElementById("pw").type = "password";
		$("#pwEye > svg").addClass("fa-eye");
		$("#pwEye > svg").removeClass("fa-eye-slash");
		pMouseDown = false;
	}
}

//let retrieveSaltAndSvrPubKey = () => {
//    var xhttp = new XMLHttpRequest();
//    xhttp.onreadystatechange = function () {
//        if (this.readyState == 4 && this.status == 200) {
//            console.log(this.responseText);
//            step2();
//        }
//    };
//    xhttp.open("POST", "getSalt", true);
//    xhttp.setRequestHeader("Content-type", "application/json");
//    xhttp.send(document.getElementById("email").value);
//  }
//
//let rmNotif = (el) => {
//    $(el).parent().remove();
//}

/*
function retrieveSaltAndSvrPubKey() {
    const email = document.getElementById("email").value;
    $.ajax({
        type: 'POST',
        url: "{% url 'retrieveSaltPubKey' %}",
        data: {"email": email},
        success: function (response) {
            compute(email, document.getElementById("pass").value, response[0], response[1])
        },
        error: function (response) {
            console.log(response)
        }
    });
};

function compute(email, password, salt, svrPubKey) {
    var clientPasswordVerifier = hashfunction(password + salt);
    $.ajax({
        type: 'POST',
        url: "{% url 'login' %}",
        data: {"email": email,
               "clientPubKey" : ,
               "M1" : },
        success: function (response) {
            alert("oh boy");
        },
        error: function (response) {
            console.log(response)
        }
    });
};*/

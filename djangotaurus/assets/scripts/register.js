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
	$("#cpwEye").on("touchstart mousedown", function (event) {
		event.stopImmediatePropagation();
		cpMouseDown = true;
		setTimeout(resetEye, 1000);
		toggleEye(document.getElementById("cpwEye"));
	});
	$("#cpwEye").on("touchend mouseup", function (event) {
		event.stopImmediatePropagation();
		if (cpMouseDown) {
			toggleEye(document.getElementById("cpwEye"));
		} else {
			cpMouseDown = false;
		}
	});

	$("#dob").flatpickr({
		dateFormat: "d/m/Y",
		maxDate: "today",
	});
	$("#btnRegister").click(function(){
        if(formValid.every((e) => e === true)){
			if(grecaptcha.getResponse().length>0){
				$.getScript(pake_url);
			}
			else{
				alert("Please complete the captcha.");
			}
        }
        else{
            document.getElementById("register-form").reportValidity();
        }
    });
	$(".flatpickr-mobile").change(() => {
		doValidate(document.getElementsByClassName("flatpickr-mobile"));
	});
});
let pMouseDown = false;
let cpMouseDown = false;
let formValid = [false, false, false, false, false, false,false];
let doValidate = (el) => {
	const $this = $(el);
	switch ($this.attr("type")) {
		case "text":
			switch ($this.attr("id")) {
				case "fn":
					formValid[0] = validateText($this.val().toLowerCase());
					setInputBehaviour($this, formValid[0]);
					break;
				case "ln":
					formValid[1] = validateText($this.val().toLowerCase());
					setInputBehaviour($this, formValid[1]);
					break;
				case "dob":
					formValid[2] = validateDob($this.val());
					setInputBehaviour($this, formValid[2]);
					break;
				case "pw":
					formValid[4] = validatePw($this.val());
					setInputBehaviour($this, formValid[4]);
					break;
				case "cpw":
					formValid[5] = validatePw($this.val());
					formValid[5] = setInputBehaviour($this, formValid[5]);
					break;
			}
			break;
		case "email":
			formValid[3] = validateEmail($this.val().toLowerCase());
			setInputBehaviour($this, formValid[3]);
			break;
		case "password":
			switch ($this.attr("id")) {
				case "pw":
					formValid[4] = validatePw($this.val());
					setInputBehaviour($this, formValid[4]);
					break;
				case "cpw":
					formValid[5] = validatePw($this.val());
					formValid[5] = setInputBehaviour($this, formValid[5]);
					break;
			}
			break;
		case "date":
			formValid[2] = validateMobileDob($this.val(),$("#dob").val());
			setInputBehaviour($this, formValid[2]);
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnRegister").attr("disabled", false)
		: $("#btnRegister").attr("disabled", true);
};

let validateText = (val) => {
	return /^([a-zA-Z]+\s)*[a-zA-Z]{2,45}$/.test(val);
};

let validateDob = (val) => {
	let match = /^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$/.test(
		val
	)
	if (match){
		return validAge(val);
	}
	return false;
};

let validateMobileDob = (val,val2) => {
	let matchMobile = /^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$/.test(val);
	let matchDesktop = /^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$/.test(val2);
	if (matchMobile && matchDesktop){
		return validAge(val2);
	}
	return false;
};

let validAge = (val) =>{
	let date = val.trim();
	let dateParts = date.split("/");
	let ISODate = new Date(dateParts[2],dateParts[1]-1,dateParts[0])
	let today = new Date();
	let age = today.getFullYear() - ISODate.getFullYear();
	var m = today.getMonth() - ISODate.getMonth();
	if (m < 0 || (m === 0 && today.getDate() < ISODate.getDate())) {
		age--;
	}
	if (age >= 16){
		return true;
	}
	return false;
}

let validateEmail = (val) => {
	return /^(([a-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
		val
	);
};

let validatePw = (val) => {
	resetPwn();
	return /^.{8,256}$/.test(val);
};

let setInputBehaviour = ($this, val) => {
	if ($this.attr("id") === "cpw") {
		val ? (val = checkSamePw()) : val;
		if (val){
			$(".pwn-step1").removeClass("is-hidden")
			doPwn();
		}
		else{
			$(".pwn-step1").addClass("is-hidden");
		}
	}
	val ? $this.removeClass("is-danger") : $this.addClass("is-danger");
	return val;
};

let checkSamePw = () => {
	let result = $("#pw").val() === $("#cpw").val();
	let msg = "Those passwords didn’t match. Try again.";
	result ? hideErrorMsg() : showErrorMsg(msg);
	return result;
};

let showErrorMsg = (msg) => {
	$("#error_text").text(msg);
	$("#error_text").removeClass("is-hidden");
};

let hideErrorMsg = () => {
	$("#error_text").addClass("is-hidden");
};

let doPwn = () => {
	$(".pwn-step1").addClass("is-hidden");
	$(".pwn-step2").removeClass("is-hidden");
	checkPwn($("#pw").val());
};

let validatePwnItem = (val) =>{
    return /(?:[A-Z\d]{35}:\d+(\r)?(\n)?)+/.test(val);
}

let checkPwn = (input) => {
    let hashed = SHA1(input.trim());
    const initial = hashed.substring(0, 5).toUpperCase();
    const toMatch = hashed.substring(5).toUpperCase();
    let cleanArray;
    let result;

    fetch("https://api.pwnedpasswords.com/range/" + initial)
        .then((response) => response.text())
        .then((data) => data.split("\n"))
        .then((arr) => {
            let regResult = arr.every((ele)=>{
                if (validatePwnItem(ele)){
                    return true;
                }
                else{
                    throw false
                }
            });
            if(regResult){
                return arr
            }
            else{
                throw new Error("API Data is invalid/tampered with");
            }
        })
        .catch(err=> console.log(err))
        .then(
            (dataArray) =>
                (cleanArray = dataArray.map((ele) => {
                    return ele.trim().replace(/:(.*)/, "");
                }))
        )
        .then(() => (result = cleanArray.some((ele) => ele === toMatch)))
        .then(() => setPwnResultBehaviour(result));
};

let setPwnResultBehaviour = (isPwned) => {
	$(".pwn-step2").addClass("is-hidden");
	if (isPwned){
		formValid[6] = false;
		$(".pwn-step3-danger").removeClass("is-hidden");
	}
	else{
		formValid[6] = true;
		$(".pwn-step3-good").removeClass("is-hidden");
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnRegister").attr("disabled", false)
		: $("#btnRegister").attr("disabled", true);
};

let resetPwn = () => {
	$(".pwn-container")
		.children("div")
		.each(function () {
			$(this).hasClass("is-hidden") ? true : $(this).addClass("is-hidden");
		});
};

let toggleEye = (ele) => {
	const pw = document.getElementById("pw");
	const cpw = document.getElementById("cpw");
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
	} else {
		if (cpw.type === "password") {
			cpw.type = "text";
			$(id + "> svg").toggleClass("fa-eye");
			$(id + "> svg").toggleClass("fa-eye-slash");
		} else {
			cpw.type = "password";
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
	else if (cpMouseDown){
		document.getElementById("cpw").type = "password";
		$("#cpwEye > svg").addClass("fa-eye");
		$("#cpwEye > svg").removeClass("fa-eye-slash");
		cpMouseDown = false;
	}
}

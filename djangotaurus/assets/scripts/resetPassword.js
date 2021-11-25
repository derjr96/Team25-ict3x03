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
    $("#btnConfirm").click(function(){
		if(formValid.every((e) => e === true)){
            $.getScript(pake_url);
        }
        else{
            document.getElementById("resetPw-form").reportValidity();
        }
    });
});
let pMouseDown = false;
let cpMouseDown = false;
let formValid = [false, false, false];
let doValidate = (el) => {
	const $this = $(el);
	switch ($this.attr("type")) {
		case "text":
			switch ($this.attr("id")) {
                case "pw":
					formValid[0] = validatePw($this.val());
					setInputBehaviour($this, formValid[0]);
					break;
				case "cpw":
					formValid[1] = validatePw($this.val());
					setInputBehaviour($this, formValid[1]);
					break;
			}
			break;
		case "password":
			switch ($this.attr("id")) {
                case "pw":
					formValid[0] = validatePw($this.val());
					setInputBehaviour($this, formValid[0]);
					break;
				case "cpw":
					formValid[1] = validatePw($this.val());
					setInputBehaviour($this, formValid[1]);
					break;
			}
			break;
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnConfirm").attr("disabled", false)
		: $("#btnConfirm").attr("disabled", true);
};

let validateText = (val) => {
	return /^[a-zA-Z]{2,45}$/.test(val);
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
		formValid[2]=false;
		$(".pwn-step3-danger").removeClass("is-hidden");
	}
	else{
		formValid[2]=true;
		$(".pwn-step3-good").removeClass("is-hidden");
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnConfirm").attr("disabled", false)
		: $("#btnConfirm").attr("disabled", true);
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
	} else if ($(ele).siblings().is(cpw)){
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

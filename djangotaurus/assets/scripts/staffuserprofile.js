//validation
let formValid = [false];
let doValidate = (el) => {
	let $this = $(el);
	switch ($this.attr("id")) {
		case "deposit":
            formValid[0] = validateDeposit($this.val().trim());
            setInputBehaviour($this, formValid[0]);
            break;
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnSave").attr("disabled", false)
		: $("#btnSave").attr("disabled", true);
};

let validateDeposit = (val) =>{
    return /^([1-4][0-9][0-9](\.\d{1,2})?|500(\.00)?)$/.test(val);
}

let setInputBehaviour = ($this, val) => {
	val ? $this.removeClass("is-danger") : $this.addClass("is-danger");
	return val;
};

let rmNotif = (el) => {
    $(el).parent().remove();
}

let showErrorMsg = (msg) => {
	$("#error_text").text(msg);
	$("#error_text").removeClass("is-hidden");
};

let hideErrorMsg = () => {
	$("#error_text").addClass("is-hidden");
};

//button behaviours
$(document).ready(()=> {
    $("#btnReset").click(() =>{
        $("html").addClass("is-clipped");
        $("#modal").addClass("is-active");
    })
    $(".delete").click(() => {
        $("html").removeClass("is-clipped");
        $("#modal").removeClass("is-active");
    });
    $("#btnConfirmCancel").click(() =>{
        $("html").removeClass("is-clipped");
        $("#modal").removeClass("is-active");
    });
    
    donutChart(investedIndustry, colorArray,chartTitle);
});

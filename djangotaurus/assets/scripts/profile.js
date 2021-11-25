let formValid = [true, true];
let doValidate = (el) => {
	let $this = $(el);
	switch ($this.attr("id")) {
		case "fn":
				formValid[0] = validateText($this.val().toLowerCase());
				setInputBehaviour($this, formValid[0]);
				break;
		case "ln":
			formValid[1] = validateText($this.val().toLowerCase());
			setInputBehaviour($this, formValid[1]);
			break;
	}
	let result = formValid.every((e) => e === true);
	result
		? $("#btnSave").attr("disabled", false)
		: $("#btnSave").attr("disabled", true);
};
let validateText=(val)=>{
	return /^([a-zA-Z]+\s)*[a-zA-Z]{2,45}$/.test(val);
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
$(document).ready(() => {
	$("#btnEdit").click(() => {
		$("#fn").attr("disabled", false);
		$("#ln").attr("disabled", false);
		$("#btnSave").removeClass("is-hidden");
		$("#btnCancel").removeClass("is-hidden");
		$("#btnDelete").removeClass("is-hidden");
		$("#btnEdit").addClass("is-hidden");
		$("#btnChangePw").addClass("is-hidden");
	});
	$("#btnCancel").click(() => {
		$("#fn").attr("disabled", true);
		$("#ln").attr("disabled", true);
		$("#btnSave").addClass("is-hidden");
		$("#btnCancel").addClass("is-hidden");
		$("#btnDelete").addClass("is-hidden");
		$("#btnEdit").removeClass("is-hidden");
		$("#btnChangePw").removeClass("is-hidden");
	});
	$("#btnDelete").click(() => {
		$("html").addClass("is-clipped");
		$("#modal").addClass("is-active");
	});
	$(".delete").click(() => {
		$("html").removeClass("is-clipped");
		$("#modal").removeClass("is-active");
	});
	$("#btnConfirmCancel").click(() => {
		$("html").removeClass("is-clipped");
		$("#modal").removeClass("is-active");
	});

    donutChart(investedIndustry, colorArray,chartTitle);
});

let setTab = (el) =>{
    const $this = $(el);
    if ($this.hasClass('is-active')){
        return 0;
    }
    else{
        let prev = $this.parent().children('.is-active');
        let prevContent = $(prev).data("target");
        $(prev).removeClass("is-active");
        $(prevContent).addClass("is-hidden");

        $this.addClass("is-active");
        let target = $this.data("target");
        $(target).removeClass("is-hidden");
    }
}
